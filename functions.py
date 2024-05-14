def draw_court(ax=None, color='black', lw=2, outer_lines=False):
    from matplotlib.patches import Circle, Rectangle, Arc
    import matplotlib.pyplot as plt
    if ax is None:
        ax = plt.gca()


    # Create the basketball hoop
    # Diameter of a hoop is 18" so it has a radius of 9", which is a value
    # 7.5 in our coordinate system
    hoop = Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False)

    # Create backboard
    backboard = Rectangle((-30, -7.5), 60, -1, linewidth=lw, color=color)

    # The paint
    # Create the outer box 0f the paint, width=16ft, height=19ft
    outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color,
                          fill=False)
    # Create the inner box of the paint, widt=12ft, height=19ft
    inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color,
                          fill=False)

    # Create free throw top arc
    top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180,
                         linewidth=lw, color=color, fill=False)
    # Create free throw bottom arc
    bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0,
                            linewidth=lw, color=color, linestyle='dashed')
    # Restricted Zone, it is an arc with 4ft radius from center of the hoop
    restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw,
                     color=color)

    # Three point line
    # Create the side 3pt lines, they are 14ft long before they begin to arc
    corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw,
                               color=color)
    corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
    # 3pt arc - center of arc will be the hoop, arc is 23'9" away from hoop
    # I just played around with the theta values until they lined up with the 
    # threes
    three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw,
                    color=color)

    # Center Court
    center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0,
                           linewidth=lw, color=color)
    center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0,
                           linewidth=lw, color=color)

    # List of the court elements to be plotted onto the axes
    court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw,
                      bottom_free_throw, restricted, corner_three_a,
                      corner_three_b, three_arc, center_outer_arc,
                      center_inner_arc]

    if outer_lines:
        # Draw the half court line, baseline and side out bound lines
        outer_lines = Rectangle((-250, -47.5), 500, 470, linewidth=lw,
                                color=color, fill=False)
        court_elements.append(outer_lines)

    # Add the court elements onto the axes
    for element in court_elements:
        ax.add_patch(element)

    return ax


def arremessos_por_temporada(jogador, temporada):
    import pandas as pd

    from nba_api.stats.static import players
    from nba_api.stats.endpoints import playercareerstats
    from nba_api.stats.endpoints import shotchartdetail
    id_jogador = players.find_players_by_full_name(jogador)[0]['id']

    df_carreira = playercareerstats.PlayerCareerStats(player_id=id_jogador).get_data_frames()[0]
    df_carreira = df_carreira.query('SEASON_ID == @temporada')

    id_time = df_carreira['TEAM_ID'].values

    if len(id_time) > 1:   
        id_time = 0        # o ID '0' representa o total em todos os times que o jogador passou

    
    df_shotchart = shotchartdetail.ShotChartDetail(player_id=id_jogador, team_id=id_time, 
                                   season_type_all_star='Regular Season', season_nullable=temporada, 
                                   context_measure_simple='FGA').get_data_frames()[0] 
    
    return df_shotchart

def gerar_grafico(df_de_arremessos):
    import matplotlib.pyplot as plt
    import seaborn as sns
    arremessos_certos = df_de_arremessos.query('SHOT_MADE_FLAG == 1')
    arremessos_errados = df_de_arremessos.query('SHOT_MADE_FLAG == 0')
    
    plt.figure(figsize=(7, 8))
    plt.ylim(480, -80)

    draw_court(outer_lines=True, color="black")

    sns.scatterplot(x=arremessos_certos.LOC_X, y=arremessos_certos.LOC_Y, 
                    data=df_de_arremessos, 
                    color='green', 
                    label='Arremessos Certos')

    sns.scatterplot(x=arremessos_errados.LOC_X, y=arremessos_errados.LOC_Y, 
                    data=df_de_arremessos, 
                    color='red', 
                    label='Arremessos Errados')

    plt.legend(loc='lower right')
    plt.axis('off')
    imagem = plt.savefig('imagem.png')

    return imagem