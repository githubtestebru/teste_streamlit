import streamlit as st
from functions import arremessos_por_temporada, gerar_grafico

st.title('Gerador de Mapa de Arremessos')

jogador = st.text_input('Digite aqui o nome do jogador:')
temporada = st.text_input('Digite aqui a temporada:')

if temporada:
    resultado = st.button('Gerar')

    if resultado:
        df = arremessos_por_temporada(jogador=jogador, temporada=temporada)
        gerar_grafico(df_de_arremessos=df)

        st.markdown(f'#### Esse foi o mapa de arremesso do {jogador} na temporada regular de {temporada}:')
        st.image('imagem.png')

        with open('imagem.png', 'rb') as file:
            st.download_button('Clique aqui para fazer donwload da imagem',
                               file_name=f'mapa_arremessos-{jogador}, {temporada}.png',
                               data=file,
                               mime='image/png')

else:
    st.warning('Digite jogador e temporada válidos.')