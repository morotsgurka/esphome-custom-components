from esphome import automation, pins
from esphome.components import stepper, uart, binary_sensor, text_sensor
from esphome.components.stepper import validate_speed
import esphome.config_validation as cv
import esphome.codegen as cg
from esphome.const import (
    CONF_CHANNEL,
    CONF_ADDRESS,
    CONF_ID,
    CONF_ENABLE_PIN,
)

AUTO_LOAD = ["text_sensor"]


tmc_ns = cg.esphome_ns.namespace("tmc")
TMC2209 = tmc_ns.class_("TMC2209", stepper.Stepper, cg.Component)
TMC2209ConfigureAction = tmc_ns.class_("TMC2209ConfigureAction", automation.Action)

CONF_DIAG_PIN = "diag_pin"
CONF_INDEX_PIN = "index_pin"
CONF_DIAG = "diagnostics"
CONF_INDEX_SENSOR = "index_sensor"
CONF_VERSION_SENSOR = "version_sensor"

CONF_VELOCITY = "velocity"
CONF_MICROSTEPS = "microsteps"
CONF_TCOOLTHRS = "tcool_threshold"
CONF_SGTHRS = "stall_threshold"
CONF_INVERSE_DIRECTION = "inverse_direction"
CONF_RUN_CURRENT = "run_current"
CONF_HOLD_CURRENT = "hold_current"
CONF_HOLD_CURRENT_DELAY = "hold_current_delay"
CONF_POWER_DOWN_DELAY = "power_down_delay"
CONF_TSTEP = "tstep"
CONF_TPWMTHRS = "tpwmthrs"

CONF_COOLCONF_SEIMIN = "coolstep_seimin"
CONF_COOLCONF_SEDN1 = "coolstep_sedn1"
CONF_COOLCONF_SEDN0 = "coolstep_sedn0"
CONF_COOLCONF_SEDN1 = "coolstep_sedn1"
CONF_COOLCONF_SEMAX3 = "coolstep_semax3"
CONF_COOLCONF_SEMAX2 = "coolstep_semax2"
CONF_COOLCONF_SEMAX1 = "coolstep_semax1"
CONF_COOLCONF_SEMAX0 = "coolstep_semax0"
CONF_COOLCONF_SEUP1 = "coolstep_seup1"
CONF_COOLCONF_SEUP0 = "coolstep_seup0"
CONF_COOLCONF_SEMIN3 = "coolstep_semin3"
CONF_COOLCONF_SEMIN2 = "coolstep_semin2"
CONF_COOLCONF_SEMIN1 = "coolstep_semin1"
CONF_COOLCONF_SEMIN0 = "coolstep_semin0"


CONF_VERSION_TEXT_SENSOR = "version_text_sensor"


CONFIG_SCHEMA = (
    stepper.STEPPER_SCHEMA.extend(
        {
            cv.Required(CONF_ID): cv.declare_id(TMC2209),
            cv.Optional(CONF_CHANNEL, default=0): cv.positive_int,
            cv.Optional(CONF_ADDRESS, default=0): cv.hex_uint8_t,
            cv.Optional(CONF_ENABLE_PIN): pins.gpio_output_pin_schema,
            cv.Required(CONF_INDEX_PIN): pins.internal_gpio_input_pin_schema,
            cv.Required(CONF_DIAG_PIN): pins.internal_gpio_input_pin_schema,
            cv.Optional(CONF_VERSION_TEXT_SENSOR): text_sensor.text_sensor_schema(),
        },
    )
    .extend(cv.COMPONENT_SCHEMA)
    .extend(uart.UART_DEVICE_SCHEMA)
    .extend(cv.polling_component_schema("60s"))
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await stepper.register_stepper(var, config)
    await uart.register_uart_device(var, config)

    if CONF_ENABLE_PIN in config:
        enable_pin = await cg.gpio_pin_expression(config[CONF_ENABLE_PIN])
        cg.add(var.set_enable_pin(enable_pin))

    if CONF_INDEX_PIN in config:
        index_pin = await cg.gpio_pin_expression(config[CONF_INDEX_PIN])
        cg.add(var.set_index_pin(index_pin))

    if CONF_DIAG_PIN in config:
        diag_pin = await cg.gpio_pin_expression(config[CONF_DIAG_PIN])
        cg.add(var.set_diag_pin(diag_pin))

    if CONF_VERSION_TEXT_SENSOR in config:
        version_text_sensor_var = await text_sensor.new_text_sensor(
            config[CONF_VERSION_TEXT_SENSOR]
        )
        # await text_sensor.register_text_sensor(
        #     version_text_sensor_var, config[CONF_VERSION_TEXT_SENSOR]
        # )
        cg.add(var.set_version_text_sensor(version_text_sensor_var))

    cg.add_library(
        "https://github.com/slimcdk/TMC-API", "3.5.1"
    )  # fork of https://github.com/trinamic/TMC-API with platformio library indexing


@automation.register_action(
    "tmc2209.configure",
    TMC2209ConfigureAction,
    cv.Schema(
        {
            cv.GenerateID(): cv.use_id(TMC2209),
            # Velocity
            cv.Optional(CONF_INVERSE_DIRECTION): cv.templatable(cv.boolean),
            cv.Optional(CONF_VELOCITY): cv.templatable(
                cv.int_range(min=-8388608, max=8388608),
            ),
            cv.Optional(CONF_HOLD_CURRENT): cv.templatable(
                cv.int_range(min=0, max=2**5, max_included=False),
            ),
            cv.Optional(CONF_RUN_CURRENT, default=31): cv.templatable(
                cv.int_range(min=0, max=2**5, max_included=False),
            ),
            cv.Optional(CONF_HOLD_CURRENT_DELAY): cv.templatable(
                cv.int_range(min=0, max=2**4, max_included=False),
            ),
            cv.Optional(CONF_POWER_DOWN_DELAY): cv.templatable(
                cv.int_range(
                    min=0, max=2**8, max_included=False
                ),  # TODO: input value in time / duration format
            ),
            # Microstepping
            cv.Optional(CONF_MICROSTEPS): cv.templatable(
                cv.one_of(256, 128, 64, 32, 16, 8, 4, 2, 0)
            ),
            cv.Optional(CONF_TCOOLTHRS): cv.templatable(
                cv.int_range(min=0, max=2**20, max_included=False)
            ),
            cv.Optional(CONF_SGTHRS): cv.templatable(
                cv.int_range(min=0, max=2**8, max_included=False)
            ),
            cv.Optional(CONF_TSTEP): cv.templatable(
                cv.int_range(min=0, max=2**20, max_included=False)
            ),
            # CoolStep configuration
            cv.Optional(CONF_COOLCONF_SEIMIN): cv.templatable(cv.boolean),
            cv.Optional(CONF_COOLCONF_SEDN1): cv.templatable(cv.boolean),
            cv.Optional(CONF_COOLCONF_SEDN0): cv.templatable(cv.boolean),
            cv.Optional(CONF_COOLCONF_SEDN1): cv.templatable(cv.boolean),
            cv.Optional(CONF_COOLCONF_SEMAX3): cv.templatable(cv.boolean),
            cv.Optional(CONF_COOLCONF_SEMAX2): cv.templatable(cv.boolean),
            cv.Optional(CONF_COOLCONF_SEMAX1): cv.templatable(cv.boolean),
            cv.Optional(CONF_COOLCONF_SEMAX0): cv.templatable(cv.boolean),
            cv.Optional(CONF_COOLCONF_SEUP1): cv.templatable(cv.boolean),
            cv.Optional(CONF_COOLCONF_SEUP0): cv.templatable(cv.boolean),
            cv.Optional(CONF_COOLCONF_SEMIN3): cv.templatable(cv.boolean),
            cv.Optional(CONF_COOLCONF_SEMIN2): cv.templatable(cv.boolean),
            cv.Optional(CONF_COOLCONF_SEMIN1): cv.templatable(cv.boolean),
            cv.Optional(CONF_COOLCONF_SEMIN0): cv.templatable(cv.boolean),
        }
    ),
)
def tmc2209_configure_to_code(config, action_id, template_arg, args):
    var = cg.new_Pvariable(action_id, template_arg)
    yield cg.register_parented(var, config[CONF_ID])
    if CONF_INVERSE_DIRECTION in config:
        template_ = yield cg.templatable(config[CONF_INVERSE_DIRECTION], args, bool)
        cg.add(var.set_inverse_direction(template_))

    if CONF_VELOCITY in config:
        template_ = yield cg.templatable(config[CONF_VELOCITY], args, int)
        cg.add(var.set_velocity(template_))

    if CONF_HOLD_CURRENT in config:
        template_ = yield cg.templatable(config[CONF_HOLD_CURRENT], args, int)  # float)
        cg.add(var.set_hold_current(template_))

    if CONF_RUN_CURRENT in config:
        template_ = yield cg.templatable(config[CONF_RUN_CURRENT], args, int)  # float)
        cg.add(var.set_run_current(template_))

    if CONF_HOLD_CURRENT_DELAY in config:
        template_ = yield cg.templatable(
            config[CONF_HOLD_CURRENT_DELAY], args, int
        )  # float)
        cg.add(var.set_hold_current_delay(template_))

    if CONF_MICROSTEPS in config:
        template_ = yield cg.templatable(config[CONF_MICROSTEPS], args, int)
        cg.add(var.set_microsteps(template_))

    if CONF_TCOOLTHRS in config:
        template_ = yield cg.templatable(config[CONF_TCOOLTHRS], args, int)
        cg.add(var.set_tcool_threshold(template_))

    if CONF_SGTHRS in config:
        template_ = yield cg.templatable(config[CONF_SGTHRS], args, int)
        cg.add(var.set_stall_threshold(template_))

    yield var
