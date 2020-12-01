
import pandas as pd
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import Image
colors = {
        'QB':'red', # Quarter Back - O
        'RB':'gold', # Running Back aka HB- O
        'HB':'gold', # Halfback aka RB - O
        'WR':'orange', # Wide Reciever -O
        'TE':'khaki', # Tight End - O
        'FB':'goldenrod', # Full back - O
        'P':'pink', # Punter - O
        'LS':'orchid', # Long Snapper - O
        'K':'plum', # Kicker -O
        'DB':'mediumorchid', # Defensive Back - D
        'S':'powderblue', # Safety - D
        'SS':'powderblue', # Strong Safety - D
        'FS':'powderblue', # Free Safety - D
        'CB':'cyan', # Corner Back - D
        'DL':'cornflowerblue', # Defensive Line -D
        'NT':'cornflowerblue', # Nose tackle - D
        'DE':'cornflowerblue', # Defensive End - D
        'DT':'cornflowerblue', # Defensive Tackle - D
        'LB':'skyblue', # Line backer - D
        'OLB':'skyblue', # Outside Line Backer - D
        'MLB':'skyblue', # Middle Line Backer - D
        'ILB':'skyblue', # Inside Line Backers - D
        'Football':'white'
        }
o_positions = {'QB','RB','HB','WR','TE','FB','P','LS','K'}
weeks = list()
#16-18
#1-10
#10-16
for x in range(1,12):
    file = 'week'+str(x)+'.csv'
    weeks.append(pd.read_csv(file))
    
weekdf = pd.concat(weeks)
plays = pd.read_csv('plays.csv')

plays = plays[['gameId', 'playId', 'passResult', 'playDescription']]
plays = plays[plays.passResult.notnull()]
plays = plays[plays.passResult != 'C']

weekdf.loc[weekdf.displayName == 'Football', 'position'] = 'Football'
weekdf = weekdf[['playId','gameId','event','frameId','position','x','y']]
result = pd.merge(weekdf, plays, on=['gameId','playId'])

#create football field representation
def create_football_field(linenumbers=True,
                          endzones=True,
                          highlight_line=False,
                          highlight_line_number=50,
                          highlighted_name='Line of Scrimmage',
                          fifty_is_los=False,
                          figsize=(12, 6.33)):
    """
    Function that plots the football field for viewing plays.
    Allows for showing or hiding endzones.
    """
    rect = patches.Rectangle((0, 0), 120, 53.3, linewidth=0.1,
                             edgecolor='r', facecolor='darkgreen', zorder=0)

    fig, ax = plt.subplots(1, figsize=figsize)
    ax.add_patch(rect)

    plt.plot([10, 10, 10, 20, 20, 30, 30, 40, 40, 50, 50, 60, 60, 70, 70, 80,
              80, 90, 90, 100, 100, 110, 110, 120, 0, 0, 120, 120],
             [0, 0, 53.3, 53.3, 0, 0, 53.3, 53.3, 0, 0, 53.3, 53.3, 0, 0, 53.3,
              53.3, 0, 0, 53.3, 53.3, 0, 0, 53.3, 53.3, 53.3, 0, 0, 53.3],
             color='white')
    if fifty_is_los:
        plt.plot([60, 60], [0, 53.3], color='gold')
        plt.text(62, 50, '<- Player Yardline at Snap', color='gold')
    # Endzones
    if endzones:
        ez1 = patches.Rectangle((0, 0), 10, 53.3,
                                linewidth=0.1,
                                edgecolor='r',
                                facecolor='blue',
                                alpha=0.2,
                                zorder=0)
        ez2 = patches.Rectangle((110, 0), 120, 53.3,
                                linewidth=0.1,
                                edgecolor='r',
                                facecolor='blue',
                                alpha=0.2,
                                zorder=0)
        ax.add_patch(ez1)
        ax.add_patch(ez2)
    plt.xlim(0, 120)
    plt.ylim(-5, 58.3)
    plt.axis('off')
    if linenumbers:
        for x in range(20, 110, 10):
            numb = x
            if x > 50:
                numb = 120 - x
            plt.text(x, 5, str(numb - 10),
                     horizontalalignment='center',
                     fontsize=20,  # fontname='Arial',
                     color='white')
            plt.text(x - 0.95, 53.3 - 5, str(numb - 10),
                     horizontalalignment='center',
                     fontsize=20,  # fontname='Arial',
                     color='white', rotation=180)
    if endzones:
        hash_range = range(11, 110)
    else:
        hash_range = range(1, 120)

    for x in hash_range:
        ax.plot([x, x], [0.4, 0.7], color='white')
        ax.plot([x, x], [53.0, 52.5], color='white')
        ax.plot([x, x], [22.91, 23.57], color='white')
        ax.plot([x, x], [29.73, 30.39], color='white')

    if highlight_line:
        hl = highlight_line_number + 10
        plt.plot([hl, hl], [0, 53.3], color='yellow')
        plt.text(hl + 2, 50, '<- {}'.format(highlighted_name),
                 color='yellow')
    return fig, ax



def saveImg(play, imgID):
  # plot positions
  fig, ax = create_football_field()
  for n, grp in play.sort_values(by='position', ascending=False).groupby("position"):
      marker = ''
      if n in o_positions:
          marker = 'o'
      elif n == 'Football':
          marker = '*'
      else:
          marker = 'P'
      grp.plot(x='x', y='y', kind='scatter', ax=ax,marker=marker, color=colors[n], s=200, legend=n)
  # plot football
  #plt.title(play1['passResult'].iloc[0]+  ' --- '+play1['playDescription'].iloc[0])
  #pr = play['passResult'].iloc[0]
  #plt.title('Example Image \n Pass Result: {0}'.format(pr))
  plt.savefig('newImgs\\'+str(imgID))
  Image.PIL.Image.open("sample.png").convert("L").save('bw.png')
  plt.clf()
  plt.close()
  
  
  

# main functions
ids = list() # unique id that is comprised of the game and play Id
values = list() # the result of the play. C = complete, S = sack, I = incomplete
for gameId, group in result.groupby('gameId'):
  for playId, play in group.groupby('playId'):
      play1 =pd.DataFrame()
      pf= play[play.event=="ball_snap" ]
    
      if('pass_forward' in play['event'].iloc[:].tolist()):
            pf= play[play.event=="pass_forward" ]
            FID = pf['frameId'].iloc[0]
            play1= play[play.frameId == (FID )]
            
      else:
            FID = math.floor(max(play['frameId']) * .3)
            play1= play[play.frameId == FID]
            
      id = str(play1['playId'].iloc[0]) +'_'+ str(pf['gameId'].iloc[0])
      id = id + '_g'
      saveImg(play1,id,cmap='gray')
      ids.append(id)
      values.append(play1['passResult'].iloc[0])
      break;

# build dataframe from results
rows = dict()
rows['id'] = ids
rows['passResult'] = values
outfile= pd.DataFrame.from_dict(rows)

#save dataframe to csv
outfile.to_csv('newImgs.csv', index=False)
      

