from esphome import pins
from esphome.components import stepper
import esphome.config_validation as cv
import esphome.codegen as cg
from esphome.const import CONF_DIR_PIN, CONF_ID, CONF_SLEEP_PIN, CONF_STEP_PIN


stepdir_ns = cg.esphome_ns.namespace("stepdir")
StepDir = stepdir_ns.class_("StepDir", stepper.Stepper, cg.Component)

CONFIG_SCHEMA = stepper.STEPPER_SCHEMA.extend(
    {
        cv.Required(CONF_ID): cv.declare_id(StepDir),
        cv.Required(CONF_STEP_PIN): pins.gpio_output_pin_schema,
        cv.Required(CONF_DIR_PIN): pins.gpio_output_pin_schema,
        cv.Optional(CONF_SLEEP_PIN): pins.gpio_output_pin_schema,
    }
).extend(cv.COMPONENT_SCHEMA)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await stepper.register_stepper(var, config)

    step_pin = await cg.gpio_pin_expression(config[CONF_STEP_PIN])
    cg.add(var.set_step_pin(step_pin))
    dir_pin = await cg.gpio_pin_expression(config[CONF_DIR_PIN])
    cg.add(var.set_dir_pin(dir_pin))

    if sleep_pin_config := config.get(CONF_SLEEP_PIN):
        sleep_pin = await cg.gpio_pin_expression(sleep_pin_config)
        cg.add(var.set_sleep_pin(sleep_pin))
