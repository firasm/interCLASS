import pylab

def arrowPlot(val,
			  valerr=None,
			  plotTitle=None,
			  rawPath=None,
			  filename='template.png'):

	if plotTitle is None:
		plotTitle = filename

	if rawPath is None:
		rawPath = '/phd/TA/Year 3 - InterClass/python/export/arrowPlots/'

	# These are the errors set up as strings

	if valerr is None:
		stringError = ['' for err in val]
	else:
		stringError = ['+/- '+str(err) for err in valerr]    	

	pylab.figure(figsize=(12,6))
	ax = pylab.subplot(111)

	# Create the boxes for each of the subjects

	ann = ax.annotate("Chemistry",
	                  xy=(0.30, 0.4), xycoords='axes fraction',
	                  size=20, va="center", ha="center",
	                  bbox=dict(boxstyle="round", fc="w")
	                  )

	ann2 = ax.annotate("Biology",
	                  xy=(0.5, 0.82), xycoords='axes fraction',
	                  size=20, va="center", ha="center",
	                  bbox=dict(boxstyle="round", fc="w")
	                  )

	ann3 = ax.annotate("Physics",
	                  xy=(0.7, 0.4), xycoords='axes fraction',
	                  size=20, va="center", ha="center",
	                  bbox=dict(boxstyle="round", fc="w")
	                  )
	pylab.xlim(0,1)
	pylab.ylim(0,1)
	pylab.grid()


	# Creating the arrows in the plot

	# Chem to Bio
	ax.annotate("",
	                  xy=(.43, 0.83),xycoords='data',
	                  xytext=(0.3, 0.47), textcoords='axes fraction',
	                  size=20, va="center", ha="center",
	                  bbox=dict(boxstyle="round", fc="w"),

	                  arrowprops=dict(arrowstyle="-|>",
	                                  connectionstyle="angle3",
	                                  fc="w"), 
	                  )

	# Bio to Chem
	ax.annotate("",
	                  xy=(0.3, 0.47),xycoords='data',
	                  xytext=(.43, 0.83), textcoords='axes fraction',
	                  size=20, va="center", ha="center",
	                  bbox=dict(boxstyle="round", fc="w"),

	                  arrowprops=dict(arrowstyle="-|>",
	                                  connectionstyle="angle3",
	                                  fc="w"), 
	                  )


	# Bio to Physics
	ax.annotate("",
	                  xy=(0.7, 0.47),xycoords='data',
	                  xytext=(0.57, 0.83), textcoords='axes fraction',
	                  size=20, va="center", ha="center",
	                  bbox=dict(boxstyle="round", fc="w"),

	                  arrowprops=dict(arrowstyle="-|>",
	                                  connectionstyle="angle3",
	                                  fc="w"), 
	                  )

	# Physics to Bio
	ax.annotate("",
	                  xy=(0.57, 0.83),xycoords='data',
	                  xytext=(.7, 0.47), textcoords='axes fraction',
	                  size=20, va="center", ha="center",
	                  bbox=dict(boxstyle="round", fc="w"),

	                  arrowprops=dict(arrowstyle="-|>",
	                                  connectionstyle="angle3",
	                                  fc="w"), 
	                  )

	# Physics to Chem
	ax.annotate("",
	                  xy=(0.39, 0.39),xycoords='data',
	                  xytext=(0.63, 0.39), textcoords='axes fraction',
	                  size=20, va="center", ha="center",
	                  bbox=dict(boxstyle="round", fc="w"),

	                  arrowprops=dict(arrowstyle="-|>",
	                                  connectionstyle="angle3,angleA=-45,angleB=45",
	                                  fc="w"), 
	                  )

	# Chem to Phys
	ax.annotate("",
	                  xy=(0.63, 0.39),xycoords='data',
	                  xytext=(.39, 0.39), textcoords='axes fraction',
	                  size=20, va="center", ha="center",
	                  bbox=dict(boxstyle="round", fc="w"),

	                  arrowprops=dict(arrowstyle="-|>",
	                                  connectionstyle="angle3,angleA=-45,angleB=45",
	                                  fc="w"), 
	                  )

	# Creating the annotations on the arrows

	# Bio to Physics
	props2 = dict(boxstyle='round', color=determine_facecolor(val[0]),alpha=1)
	ax.text(0.59,0.63,str(val[0])+stringError[0],
		size=14,ha='center', va='center',fontsize=14,
		verticalalignment='top', bbox=props2,color='w',transform=ax.transAxes)

	# Bio to Chem
	props1 = dict(boxstyle='round', color=determine_facecolor(val[1]),alpha=1)
	ax.text(0.41,0.63,str(val[1])+stringError[1],
		size=14,ha='center', va='center', fontsize=14,
		verticalalignment='top', bbox=props1,color='w',transform=ax.transAxes)

	# Chem to Bio
	props0 = dict(boxstyle='round', color=determine_facecolor(val[2]),alpha=1)
	ax.text(0.32,0.7,str(val[2])+stringError[2],
		size=14,ha='center', va='center', fontsize=14,
		verticalalignment='top', bbox=props0,color='w',transform=ax.transAxes)

	# Chem to Physics
	props5 = dict(boxstyle='round', color=determine_facecolor(val[3]),alpha=1)
	ax.text(0.51,0.3,str(val[3])+stringError[3],
		size=14,ha='center', va='center', fontsize=14,
		verticalalignment='top', bbox=props5,color='w',transform=ax.transAxes)


	# Physics to Bio
	props3 = dict(boxstyle='round', color=determine_facecolor(val[4]),alpha=1)
	ax.text(0.68,0.7,str(val[4])+stringError[4],
		size=14,ha='center', va='center', fontsize=14,
		verticalalignment='top', bbox=props3,color='w',transform=ax.transAxes)

	# Physics to Chem
	props4 = dict(boxstyle='round', color=determine_facecolor(val[5]),alpha=1)
	ax.text(0.51,0.52,str(val[5])+stringError[5],
		size=14,ha='center', va='center', fontsize=14,
		verticalalignment='top', bbox=props4,color='w',transform=ax.transAxes)


	# Export and save the image
	pylab.axis('off')
	pylab.title(plotTitle, fontsize=20)

	pylab.savefig(rawPath+filename,dpi=300,transparent=True)
	pylab.close()

	if valerr is None:
		print('Arrow plot (no error bars) saved in file: "{0}.png"'.format(filename))
	else:
		print('Arrow plot with error bars saved in file: "{0}.png"'.format(filename))


def determine_facecolor(score):

	## On a -1,0,1 point scale

    fc ='grey'
    if score < -0.1:
        fc = 'red'
    elif score>=-0.1 and score <0.1:
        fc = 'orange'
    elif score >=0.1:
        fc ='green'

    ## On a 5 point scale
    
    #fc ='grey'
    #if score < 3.2:
    #    fc = 'red'
    #elif score>=3.2 and score <4.2:
    #    fc = 'orange'
    #elif score >=4.2:
    #    fc ='green'

    return fc

### Firas Plots ###

# Currently not really working, but not really used either

"""

def chooseData(dataSource = allData,
               courseList = None,
               course = None,
               questionDict = None,
               question = None):
    
    # First get the data for the Course Name (or all data)
    
    if course is None:
        currD = dataSource
    else:
        currD = dataSource[dataSource['Course']==course]
        
    # Then get the data for the question specified        
    if question is None:
        result = currD
    else:
        result = currD[questionDict[question]]
    
    return result

def createFirasPlot(pairedQs,
                    course_interested,
                    export_filename):

    for i,q in enumerate(pairedQs.iteritems()):

        subplot(1,3,i+1)

        # Choosing the data first

        A_B = chooseData(allData,
                         courseList = courseList,
                         course = course_interested,
                         questionDict = questions,
                         question = q[1][0])

        B_A = chooseData(allData,
                         courseList = courseList,
                         course = course_interested,
                         questionDict = questions,
                         question = q[1][1])

        # Filtering out data
        A_B = A_B[A_B>0]
        B_A = B_A[B_A>0]

        gg = zip(A_B,B_A)

        xL = []
        yL = []
        area = [] 
        colour = []

        for it in Counter(gg):

            xL.append(it[0])
            yL.append(it[1])
            area.append(1e4*Counter(gg)[it]/len(gg))
            colour.append((it[0] + it[1]))

            text(it[0],it[1],
                 math.trunc(round(100.*Counter(gg)[it]/len(gg),0)),
                 size=13,horizontalalignment='center',verticalalignment='center',color='k')    

        sct = scatter(xL, yL, s=area, c = colour, linewidths=2, edgecolor='k',cmap='jet')
        sct.set_alpha(0.65)

        xlim(.5,5.5)
        ylim(.5,5.5)

        pyplot.locator_params(axis = 'x', nbins = 6)
        pyplot.locator_params(axis = 'y', nbins = 6)

        xlabel('{0}'.format(q[1][0]),size=16)
        ylabel('{0}'.format(q[1][1]),size=16)
        title('{0}'.format(q[0]),size=18)
        
        pylab.suptitle(course_interested+'\n \n \n',size=24)

        if i >2:
            text(6,4,'1 - Strongly disagree \n5- Strongly agree',size=13)

        savefig('/phd/TA/Year 3 - InterClass/python/export/Firas_plots.pdf')

    pylab.tight_layout()    


figsize(12,6)

course_interested = 'Biol 121 Pre'

pairedQs = {'Physics and Biology': ['P important for B','B important for P'],
            'Biology and Chemistry': ['B important for C','C important for B'],
            'Chemistry and Physics': ['C important for P','P important for C']}

course_interested = 'Biol 121 Pre'
createFirasPlot(pairedQs,course_interested,course_interested+'FirasPlot.pdf')


"""