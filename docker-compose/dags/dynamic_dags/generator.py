from jinja2 import Environment, FileSystemLoader
import yaml
import os

file_dir = os.path.dirname(os.path.abspath(__file__))
env = Environment(loader=FileSystemLoader(file_dir))
template = env.get_template('template_dag.jinja2')

for filename in os.listdir(file_dir):
    # loop over configuration yaml
    if filename.endswith('.yml'):
        # read configuration
        with open(f'{file_dir}/{filename}', 'r') as configfile:
            config = yaml.safe_load(configfile)
            # generate dags based on config and template
            with open(f'dags/get_price_{config["dag_id"]}.py', 'w') as file:
                file.write(template.render(config))