import pandas as pd
import random
import os
import yaml

from slugify import slugify

'''
Ideally would populate a MongoDB database. I use a CSV here for the first iteration.
'''
DATA_PATH = os.path.join('..', '_data', 'intoxicate')
kernel =yaml.safe_load(open(os.path.join(DATA_PATH, 'kernel.yml'), 'r'))
flattened_kernel = {item['variable_name']: item['variable_value'] for item in kernel}
predictive_variables = ['intoxicant', 'age', 'sbp', 'hr', 'gcs', 'second_diagnose', 'cirrhosis', 'dysrhythmia', 'respiratory'] 


def chose_variable(variable_name):
    data = yaml.safe_load(open(os.path.join(DATA_PATH, f'{variable_name}_values.yml'), 'r'))
    return random.choice(data)


def create_patient():
    ans = {}
    for variable_name in predictive_variables:
        tmp = chose_variable(variable_name)
        name = tmp['name']
        value = tmp['value']
        ans[f'{variable_name}_name'] = name
        ans[f'{variable_name}_value'] = value

    risk_score = calculate_risk_score(ans)
    ans['risk'] = risk_score
    return ans


def calculate_risk_score(patient):
    risk_score = 0
    for variable_name in predictive_variables:
        score = patient[f'{variable_name}_value']
        kernel_variable_name = slugify(variable_name.lower(), separator='_')
        if kernel_variable_name == 'CO, As, CN':
            weight = flattened_kernel['toxins_nos']
        elif kernel_variable_name == 'intoxicant':
            weight = flattened_kernel[slugify(patient['intoxicant_name'].lower(), separator='_')]
        else:
            weight = flattened_kernel[kernel_variable_name]
        risk_score += (score * weight)
    return risk_score


def split_patient(patient):
    variable_names = {key: value['name'] for key, value in patient.items()}
    variable_values = {key: value['value'] for key, value in patient.items()}
    return (variable_names, variable_values)


n_patients = 1000
# names, codes = zip(*[split_patient(create_patient()) for _ in range(n_patients)])

patient = [create_patient() for _ in range(n_patients)]

# df_codes = pd.DataFrame(codes)
# df_names = pd.DataFrame(names)
#
# df_codes.to_csv(os.path.join(DATA_PATH, 'intoxicate_codes.csv'), index=False)
# df_names.to_csv(os.path.join(DATA_PATH, 'intoxicate_names.csv'), index=False)

df = pd.DataFrame(patient)
df.to_csv(os.path.join(DATA_PATH, 'intoxicate.patient_registry.csv'), index=False)

