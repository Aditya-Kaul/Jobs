# @Reference: https://github.com/PlayingNumbers/ds_salary_proj
# @author: Ken


import pandas as pd
pd.set_option("display.max_rows", None, "display.max_columns", None)
df = pd.read_csv('glassdoor_jobs.csv')

#salary parsing
#Company name text only
#state field
#age of company
#parsing job desc and some keywords

df = df[df['Salary Estimate'] != '-1']
df['hourly'] = df['Salary Estimate'].apply(lambda a: 1 if 'per hour' in a.lower() else 0)
df['employer_provided'] = df['Salary Estimate'].apply(lambda a: 1 if 'employer provided salary:' in a.lower() else 0)

salary = df['Salary Estimate'].apply(lambda x: x.split('(')[0])

minus_kd = salary.apply(lambda y: y.replace('$','').replace('K',''))
sal_range = minus_kd.apply(lambda z: z.lower().replace('per hour','').replace('employer provided salary:',''))

df['min_salary'] = sal_range.apply(lambda x: int(x.split('-')[0]))
df['max_salary'] = sal_range.apply(lambda i: int(i.split('-')[1]))
df['avg_salary'] = (df['min_salary']+df['max_salary'])/2
df['company_txt'] = df.apply(lambda a: a['Company Name'] if int(a['Rating']) < 0 else a['Company Name'][:-3],axis = 1)
df['job_state'] = df['Location'].apply(lambda x: x.split(',')[1])
df['job_state'].value_counts()
df['same_state'] = df.apply(lambda x: 1 if x['Location'] == x['Headquarters'] else 0,axis = 1)
df['age'] = df['Founded'].apply(lambda x: x if x < 1 else 2023 - x)
df['python_yn'] = df['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)
 

df['R_yn'] = df['Job Description'].apply(lambda x: 1 if 'r studio' in x.lower() or 'r-studio' in x.lower() else 0)
df.R_yn.value_counts()


df['spark'] = df['Job Description'].apply(lambda x: 1 if 'spark' in x.lower() else 0)
df.spark.value_counts()


df['aws'] = df['Job Description'].apply(lambda x: 1 if 'aws' in x.lower() else 0)
df.aws.value_counts()


df['excel'] = df['Job Description'].apply(lambda x: 1 if 'excel' in x.lower() else 0)
df.excel.value_counts() 

df.columns
df_out = df.drop(['Unnamed: 0'], axis = 1)
df_out.to_csv('salary_data_cleaned.csv',index = False)