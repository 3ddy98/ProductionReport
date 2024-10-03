import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import datetime as dt
from datetime import timedelta
from datetime import datetime as dt2
import matplotlib.dates as mdates
import os
pd.options.mode.chained_assignment = None



class Item:
	def __init__(self,SKU,WO,Duration,Qty,Time_start,Time_end,Date_start,Date_end):
		self.SKU = SKU
		self.WO = WO
		self.Duration= Duration
		self.Qty = Qty
		self.Time_start = Time_start
		self.Time_end = Time_end
		self.Date_start = Date_start
		self.Date_end = Date_end
		self.materials = "Coming Soon"


	def print_product_data(self):
		print("SKU:",self.SKU)
		print("WO:",self.WO)
		print("Duration:",self.Duration)
		print("QTY: ",self.Qty)
		print("Time Start: ",self.Time_start)
		print("Time End: ",self.Time_end)
		print("Date Start: ",self.Date_start)
		print("Date End: ",self.Date_end)

class Production_Line:
	def __init__(self,line_ID):
		self.line_ID = ""
		self.wetpacks_produced = 0
		self.employees = 0
		self.products_worked = []
		self.average_WPH = 0

	def print_line_data(self):
		print("Line ID: ",self.line_ID)
		print("Employees: ",self.employees)
		for product in self.products_worked:
			product.print_product_data()

def generate_line_report(prod_line,line_ID,hours_worked):
	#prod_line['RealDuration(Min)'] = prod_line['RealDuration(Min)'].str.replace(',','')

	prod_line['Boxes'] = prod_line['Boxes'].astype('float64')
	prod_line['RealDuration(Min)'] = prod_line['RealDuration(Min)'].astype('float32')
	prod_line['Workers']= prod_line['Workers'].astype('float64')

	prod_line['WPH'] = np.where(prod_line['Boxes'] <= 0,0,prod_line['Boxes']/prod_line['RealDuration(Min)'])
	prod_line['WPH'] = round(prod_line['WPH'] * 60,0)

	prod_line['WPH/Person'] = np.where(prod_line['Workers']<=0,0,(prod_line['WPH']/prod_line['Workers']))
	prod_line['Boxes Produced'] = prod_line['Boxes'].cumsum()

	prod_line["TimeEnd"] = pd.to_datetime(prod_line["TimeEnd"],format="%H:%M:%S")

	#Summary Data
	max_WPH = prod_line["WPH"].max()
	min_WPH = prod_line["WPH"].min()
	avg_WPH = round(prod_line["WPH"].mean(),1)
	std_dev = round(prod_line["WPH"].std(),1)
	total_worked = prod_line["Boxes"].sum()
	skus_worked = len(prod_line["Product"])
	fastest_prod = prod_line.loc[prod_line["WPH"]==max_WPH]["Product"]
	slowest_prod = prod_line.loc[prod_line["WPH"]==min_WPH]["Product"]

	table1 = prod_line[['TimeEnd','RealDuration(Min)','Product','Boxes']]
	table2 = prod_line[['TimeEnd','Product','WPH']]

	

	#plotting Boxes Made
	fig= plt.figure(figsize=(16,9))
	date = prod_line.iloc[0]['DateBeginning']
	title = line_ID + ' ' + str(date)
	fig.suptitle(title)
	timerange = pd.date_range('1900-01-01T6:00:00.000','1900-01-01T15:00:00.000',freq="h")
	prod_line["TimeEnd"] = prod_line["TimeEnd"] - pd.Timedelta(hours=3)

	target = 0
	if line_ID == "CXLINE1":
		target_avg_wph_1=75
		target = hours_worked * target_avg_wph_1
	elif line_ID == "CXLINE2":
		target_avg_wph_2 = 110
		target = hours_worked * target_avg_wph_2
	elif line_ID == "CXLINE3":
		target_avg_wph_3 = 150
		target = hours_worked * target_avg_wph_3
	elif line_ID == "CXLINE4":
		target_avg_wph_4 = 150
		target = hours_worked * target_avg_wph_4

	data = pd.DataFrame([
		["Fastest Product",fastest_prod.values[0]],
		["Max WPH",max_WPH],
		["Slowest Product", slowest_prod.values[0]],
		["Min WPH",min_WPH],
		["Average WPH",avg_WPH],
		["STD Dev", std_dev],
		["SKUs Worked",skus_worked],
		["Hours Worked",hours_worked],
		["Production Goal: ",target],
		["Total Produced",total_worked],
		["Difference to Goal: ",total_worked-target]
		],columns=["Label","Values"])

	print("Target: ",target)
	#plotting total worked
	ax1 = fig.add_subplot(2,2,1)
	ax1.grid(visible=True)
	#prod_line["TimeEnd"] = prod_line["TimeEnd"].astype("str")
	p1 = ax1.plot(prod_line["TimeEnd"],prod_line['Boxes Produced'],"D",linestyle='solid')
	ax1.plot([min(timerange),max(timerange)],[target,target])
	for x, y, text in zip (prod_line["TimeEnd"],prod_line['Boxes Produced'],prod_line['Boxes Produced']):
		ax1.text(x,y,text)

	ax1.set_ylim(top = 3000,bottom=0)
	ax1.set_xlim(timerange.min(),timerange.max())
	#ax1.set_xticklabels(timerange,rotation = 45,fontsize="xx-small")
	ax1.set_title("Day Production ")


	#plotting rate per hour
	ax3 = fig.add_subplot(2,2,2)
	ax3.grid(visible=True)
	p3 = ax3.bar(prod_line['TimeEnd'],prod_line['WPH'],width=0.005)
	ax3.plot([min(timerange),max(timerange)],[avg_WPH,avg_WPH],color="g")
	ax3.plot([min(timerange),max(timerange)],[avg_WPH+std_dev,avg_WPH+std_dev],"--",color="y")
	ax3.plot([min(timerange),max(timerange)],[avg_WPH-std_dev,avg_WPH-std_dev],"--",color="y")
	
	#axis formatting
	ax3.set_ylim(top = 300,bottom=0)
	#ax3.set_xticks(timerange)
	ax3.set_xlim(min(timerange),max(timerange))	
	#ax3.set_xticklabels(timerange, rotation=45,fontsize="xx-small")
	ax3.set_title("Wetpacks Per Hour")
	
	#plotting products worked
	ax2 = fig.add_subplot(2,3,4)
	ax2.axis('off')
	ax2.axis('tight')
	p2 = ax2.table(cellText=table1.values,colLabels=table1.columns,loc="center")
	p2.auto_set_font_size(True)

	p2.set_fontsize(10)

	#plotting products worked
	ax5 = fig.add_subplot(2,3,5)
	ax5.axis('off')
	ax5.axis('tight')
	p5 = ax5.table(cellText=table2.values,colLabels=table2.columns,loc="center")
	p5.auto_set_font_size(True)

	p5.set_fontsize(10)

	#Day products statistics 
	ax4 = fig.add_subplot(2,3,6)
	ax4.axis('off')
	ax4.axis('tight')
	p4 = ax4.table(cellText=data.values,colLabels=data.columns,loc="center")
	p4.auto_set_font_size(True)
	

	plt.subplots_adjust(left=0.1,
                    bottom=0.2, 
                    right=0.9, 
                    top=0.9, 
                    wspace=0.1, 
                    hspace=0.3)
	filename = line_ID +" - "+ str(date)[1:10]+  '.png'
	plt.savefig('DailyReport/'+filename,dpi=300)

	with open("Report.txt","a") as f:
		f.write(50*"-")
		f.write("\n")
		f.write(line_ID)
		f.write("\n")
		f.write(data.to_string())
		f.write("\n")
		f.write(50*"-")
		f.write(4*"\n")
		f.close()

def get_prod_line_dfs(df,line_IDs):
	prod_lines_dfs= []
	for line_ID in line_IDs:
		cxline =  df.loc[(df['Line']==line_ID)]
		prod_lines_dfs.append(cxline)
	return prod_lines_dfs

def calculate_line_stats(prod_line,ID):
	#prod_line['RealDuration(Min)'] = prod_line['RealDuration(Min)'].str.replace(',','')
	prod_line['Boxes'] = prod_line['Boxes'].astype('float64')
	prod_line['RealDuration(Min)'] = prod_line['RealDuration(Min)'].astype('float32')
	prod_line['Workers']= prod_line['Workers'].astype('float64')

	prod_line['WPH'] = np.where(prod_line['Boxes'] <= 0,0,prod_line['Boxes']/prod_line['RealDuration(Min)'])
	prod_line['WPH'] = round(prod_line['WPH'] * 60,2)


	products = prod_line['Product'].unique()
	prod_line_stats = pd.DataFrame(columns=["Product"])
	for product in products:
		product_df = prod_line.loc[prod_line['Product']==product]
		average_WPH = round(product_df['WPH'].mean(),2)
		max_WPH = round(product_df['WPH'].max(),2)
		min_WPH = round(product_df['WPH'].min(),2)
		var_WPH = round(product_df['WPH'].std(),2)
		row = pd.DataFrame([[ID,product,average_WPH,max_WPH,min_WPH,var_WPH]],columns=["Line","Product","Average WPH","Max WPH","Min WPH","STD"])
		prod_line_stats = pd.concat([row,prod_line_stats],ignore_index=True)

	return prod_line_stats

def generate_line_report_monthly(all_df):
	print(all_df)
	line_stats = []
	IDs = all_df['Line'].unique()
	products = all_df['Product'].unique()
	for ID in IDs:
		prod_line_stats = calculate_line_stats(all_df.loc[all_df["Line"]==ID],ID)
		line_stats.append(prod_line_stats)


	#plotting Boxes Made
	fig= plt.figure(figsize=(16,9))
	title = "Monthly Report"
	fig.suptitle(title)
	ax1 = fig.add_subplot(1,1,1)
	ax1.set_ylim(top=300)
	ax1.set_title("Average WPH")
	#setting up time axis

	for prod_line_stats in line_stats:
	# plotting boxes produced
		print(prod_line_stats)
		scatter = ax1.scatter(prod_line_stats['Product'],prod_line_stats['Average WPH'])
	
	ax1.legend(IDs)
	# produce a legend with a cross-section of sizes from the scatter
		
		
	plt.xticks(rotation=90)
	plt.grid(visible=True,axis='both')
	plt.subplots_adjust(left=0.1,
                    bottom=0.25, 
                    right=0.9, 
                    top=0.9, 
                    wspace=0.4, 
                    hspace=0.4)
	filename = 'monthly_report.png'
	#plt.savefig(filename)
	plt.show()

def main():
	#loading report
	while 1:

		print("Production Report Generator")
		print("1) Monthly")
		print("2) Daily")
		print("3) Exit")
		print("Selection: ",end='')

		selection = int(input())

		if selection == 1:
			filenames = os.listdir("reports/")
			main_df = pd.DataFrame()
			for filename in filenames:
				df = pd.DataFrame(pd.read_excel("reports/"+filename))
				main_df = pd.concat([main_df,df],ignore_index=True)
			generate_line_report_monthly(main_df)

		elif selection == 2:	
			print("Input Filename: ",end='')
			file = str(input())
			main_df = pd.read_excel(file)
			line_IDs = main_df["Line"].unique()
			prod_lines_dfs = get_prod_line_dfs(main_df,line_IDs)
			#generate report
			for x in range(len(prod_lines_dfs)):
				print("{} Hours Work: ".format(line_IDs[x]))
				hours_worked = float(input())
				generate_line_report(prod_lines_dfs[x],line_IDs[x],hours_worked)
		elif selection == 3:
			break;
		#except:
		#	print("Something went wrong, try again")

if __name__ == "__main__":
	main()