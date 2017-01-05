import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

os.chdir(r'C:\IdeasLiberty\2048')
big_df = pd.DataFrame()
for filename in os.listdir('.'): # Join all the datasets of the methods into one
	if filename.endswith('.csv'):
		dataset = filename.split(' ')[0]
		df = pd.read_csv(filename,names = ['Attempt#','Final score', "Max tile", "Time","TimesDown"])
		df['Method'] = dataset
		big_df = big_df.append(df)

df = big_df

# Because it took 2 seconds until the stuck function activated and went down when it was stuck
df['Adjusted Time'] = df['Time']-2*df['TimesDown'] 

df['Effectiveness'] = df['Final score']/df['Adjusted Time']

score = df.pivot_table(values='Final score', index='Method', aggfunc=np.mean)
score = score[[2,0,4,3,1]]

eff = df.pivot_table(values='Effectiveness', index='Method', aggfunc=np.mean)
eff = eff[[2,0,4,3,1]]

y_pos = np.arange(len(score))

plt.figure(1)
plt.bar(y_pos, score, align='center', alpha=1,width = 1, color = 'orange')
plt.xticks(y_pos, score.index)
plt.ylabel('Score')
plt.title('Score averages by method', y=1.03)
plt.tick_params(axis='x', which='major', labelsize=12)
for a,b in zip(y_pos, score.round(2)): # Adding the values to the graph
    plt.text(a, b-400, str(b), ha='center', va='bottom')

plt.figure(2)
plt.bar(y_pos, eff, align='center', alpha=1,width = 1, color = 'orange')
plt.xticks(y_pos, eff.index)
plt.ylabel('Effectiveness (points/second)')
plt.title('Effectiveness averages by method', y=1.03)
plt.tick_params(axis='x', which='major', labelsize=12)
for a,b in zip(y_pos, eff.round(2)):
    plt.text(a, b-10, str(b), ha='center', va='bottom')

plt.show()

distribution = (df.groupby(by = 'Method')['Max tile'].value_counts()/60*100).sort_index().round(2)[['Random','Circle','TopRandom','TopCircle','FirstWin']]
distribution.to_csv('distribution.csv')