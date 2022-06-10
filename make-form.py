#!/usr/bin/env python
import os
import time
from typing import List, Dict

import jinja2
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(HERE, "config.yml")
TEMPLATE_FILE = "template.html"


def read_config(config_path: str = CONFIG_FILE):
    with open(config_path) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    return config


def _render_min_max(type_, config):
    if type_ == "number":
        min_ = config.get("min", "")
        max_ = config.get("max", "")
    else:
        min_ = config.get("min", "")
        max_ = config.get("max", "")

    min_text = ""
    if min_:
        min_text = f'min="{min_}"' if type_ == "number" else f'minlength="{min_}"'

    max_text = ""
    if max_:
        max_text = f'max="{max_}"' if type_ == "number" else f'maxlength="{max_}"'

    return f"{min_text} {max_text}"


def _render_text_like_field(name, config):
    label = config.get("label", name.capitalize())
    id_ = f"input{label}"
    type_ = config["type"]
    required = "required" if config.get("required", False) else ""
    placeholder = config.get("placeholder", label)
    read_only = "readonly" if config.get("readonly", False) else ""
    min_max = _render_min_max(type_, config)
    template = f"""
       <div class="form-group row">
          <label for="{id_}" class="col-sm-4 col-form-label">{label}</label>
          <div class="col-sm-8">
            <input type="{type_}"
                   class="form-control"
                   id="{id_}"
                   placeholder="{placeholder}"
                   name="{label}"
                   {min_max} {required} {read_only}>
          </div>
       </div>
    """
    return template.rstrip()


def _render_radio_field_item(name, config, option):
    label = option["label"]
    value = option.get("value", label.lower())
    id_ = f"{name}-{value}"
    required = "required" if config.get("required", False) else ""
    template = f"""
    <div class="form-check">
      <input class="form-check-input"
             type="radio"
             name="{name.capitalize()}"
             id="{id_}"
             value="{value}"
             {required}>
      <label class="form-check-label" for="{id_}">{label}</label>
    </div>
    """
    return template


def _render_radio_field(name, config):
    label = config.get("label", name.capitalize())
    id_ = f"input{label}"
    fieldset = "\n".join(
        _render_radio_field_item(name, config, option) for option in config["options"]
    )
    template = f"""
  <fieldset class="form-group">
    <div class="row">
      <legend class="col-form-label col-sm-4 pt-0">{label}</legend>
      <div class="col-sm-8">
      {fieldset}
      </div>
    </div>
  </fieldset>
    """
    return template


def render_form(form):
    """Render form"""
    text = ""
    for name, config in form.items():
        type_ = config.setdefault("type", "text")
        if type_ in {"text", "email", "number"}:
            form_item = _render_text_like_field(name, config)
        elif type_ == "radio":
            form_item = _render_radio_field(name, config)
        else:
            form_item = f"Could not render {name}:{type_} field!"
        text += form_item
    return text.strip()


def generate_index(config):
    output_dir = HERE
    loader = jinja2.FileSystemLoader(searchpath=HERE)
    filters = dict(render_form=render_form)
    env = jinja2.Environment(loader=loader)
    env.filters = filters
    template = env.get_template(TEMPLATE_FILE)
    output = template.render(config=config, date=time.time())
    with open(os.path.join(output_dir, "index.html"), "w") as f:
        f.write(output)
    return f.name


def main() -> None:
    config = read_config()
    generate_index(config)


if __name__ == "__main__":
    main()
