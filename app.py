import math
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Simulador de Física - Ensino Médio", layout="wide")

G = 9.8
R_GAS = 8.314
SIGMA = 5.67e-8

st.title("🎓 Simulador Interativo de Física (Ensino Médio, ENEM e Vestibulares)")
st.markdown(
    "Este app reúne **20 simuladores clássicos de Física do Ensino Médio**. "
    "Escolha um tema no menu lateral, ajuste os **sliders**, observe o **gráfico**, "
    "analise os **resultados numéricos** e confira a **interpretação física**."
)

sim = st.sidebar.selectbox("Escolha o simulador", [
    "MRU", "MRUV", "Lançamento Vertical", "Lançamento Horizontal", "Lançamento Oblíquo", "Queda Livre",
    "Força Resultante e 2ª Lei de Newton", "Plano Inclinado (com/sem atrito)", "Força Elástica (Lei de Hooke)",
    "Conservação da Energia Mecânica", "Colisões e Quantidade de Movimento", "Movimento Circular Uniforme",
    "Gravitação Universal", "Calorimetria e Equilíbrio Térmico", "Dilatação Térmica", "Transformações Gasosas",
    "Ondas em Cordas", "Efeito Doppler", "Espelhos", "Lentes"
])


def plot_xy(x, y, xlabel, ylabel, title):
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)


def questoes(base):
    st.subheader("🧠 Perguntas de fixação")
    for i, (q, a) in enumerate(base, 1):
        st.markdown(f"**{i}. {q}**")
        with st.expander("Ver gabarito"):
            st.write(a)

if sim == "MRU":
    st.header("MRU - Movimento Retilíneo Uniforme")
    s0 = st.slider("Posição inicial s0 (m)", -100.0, 100.0, 0.0)
    v = st.slider("Velocidade v (m/s)", -30.0, 30.0, 10.0)
    tmax = st.slider("Tempo máximo (s)", 1.0, 30.0, 10.0)
    t = np.linspace(0, tmax, 200); s = s0 + v*t
    plot_xy(t, s, "t (s)", "s (m)", "s = s0 + vt")
    st.metric("Posição final", f"{s[-1]:.2f} m")
    st.info("Interpretação: velocidade constante gera gráfico posição x tempo linear.")
    questoes([("Se v=0, como fica o movimento?", "Repouso."), ("Sinal de v indica?", "Sentido do movimento."), ("Inclinação da reta sxt é?", "A própria velocidade v.")])

elif sim == "MRUV":
    st.header("MRUV")
    s0 = st.slider("s0 (m)", -50.0, 50.0, 0.0); v0 = st.slider("v0 (m/s)", -30.0, 30.0, 5.0); a = st.slider("a (m/s²)", -20.0, 20.0, 2.0); tmax = st.slider("Tempo (s)", 1.0, 20.0, 8.0)
    t=np.linspace(0,tmax,200); s=s0+v0*t+0.5*a*t**2; v=v0+a*t
    c1,c2=st.columns(2); 
    with c1: plot_xy(t,s,"t","s","Posição x tempo")
    with c2: plot_xy(t,v,"t","v","Velocidade x tempo")
    st.metric("Velocidade final", f"{v[-1]:.2f} m/s")
    st.info("Interpretação: aceleração constante altera linearmente a velocidade.")
    questoes([("Se a>0 e v0>0?", "Movimento acelerado."), ("Gráfico vxt no MRUV?", "Reta."), ("Gráfico sxt no MRUV?", "Parábola.")])

else:
    st.header(sim)
    st.write("Simulador simplificado com Física de Ensino Médio.")
    x = st.slider("Parâmetro 1", 0.0, 100.0, 50.0)
    y = st.slider("Parâmetro 2", 0.0, 100.0, 20.0)
    t = np.linspace(0, 10, 200)

    if sim == "Lançamento Vertical":
        v0=x/2; h0=y/5; h=h0+v0*t-0.5*G*t**2
        plot_xy(t,h,"t(s)","h(m)","Altura x tempo")
        hmax = h0 + v0**2/(2*G)
        st.metric("Altura máxima", f"{hmax:.2f} m")
        st.info("Interpretação: sobe desacelerando, para no topo e depois cai.")
    elif sim == "Lançamento Horizontal":
        v0=x/2; h0=max(1,y/2); tx=np.sqrt(2*h0/G); alcance=v0*tx
        xx=v0*t; yy=h0-0.5*G*t**2
        plot_xy(xx,yy,"x(m)","y(m)","Trajetória")
        st.metric("Alcance aproximado", f"{alcance:.2f} m")
        st.info("Interpretação: movimento composto (MRU na horizontal + queda vertical).")
    elif sim == "Lançamento Oblíquo":
        v0=x/2; ang=math.radians(y*0.9); xx=v0*math.cos(ang)*t; yy=v0*math.sin(ang)*t-0.5*G*t**2
        plot_xy(xx,yy,"x","y","Trajetória oblíqua")
        st.metric("Alcance teórico", f"{(v0**2*math.sin(2*ang)/G):.2f} m")
        st.info("Interpretação: trajetória parabólica.")
    elif sim == "Queda Livre":
        h0=max(1,x); h=h0-0.5*G*t**2
        plot_xy(t,h,"t","h","Queda livre")
        st.metric("Tempo de queda", f"{math.sqrt(2*h0/G):.2f} s")
        st.info("Interpretação: aceleração aproximadamente constante g.")
    elif sim == "Força Resultante e 2ª Lei de Newton":
        m=max(1,x/10); F=y-30; a=F/m
        st.metric("Aceleração", f"{a:.2f} m/s²")
        plot_xy(np.array([0,1]),np.array([0,a]),"tempo","velocidade relativa","v=at")
        st.info("Interpretação: a = Fres/m.")
    elif sim == "Plano Inclinado (com/sem atrito)":
        ang=math.radians(x*0.6); mu=y/100
        a=G*(math.sin(ang)-mu*math.cos(ang))
        st.metric("Aceleração no plano", f"{a:.2f} m/s²")
        st.info("Interpretação: atrito reduz (ou impede) o deslizamento.")
    elif sim == "Força Elástica (Lei de Hooke)":
        k=max(1,x); deform=(y-50)/10; F=-k*deform
        st.metric("Força elástica", f"{F:.2f} N")
        plot_xy(np.linspace(-1,1,50),-k*np.linspace(-1,1,50),"x(m)","F(N)","F=-kx")
        st.info("Interpretação: força restauradora oposta à deformação.")
    elif sim == "Conservação da Energia Mecânica":
        m=max(1,x/10); h=max(0,y/2); Em=m*G*h; v=math.sqrt(2*G*h)
        st.metric("Energia mecânica", f"{Em:.2f} J"); st.metric("Velocidade no solo", f"{v:.2f} m/s")
        st.info("Sem dissipação, energia potencial vira cinética.")
    elif sim == "Colisões e Quantidade de Movimento":
        m1=max(1,x/10); m2=max(1,y/10); v1=10; v2=-5
        vf=(m1*v1+m2*v2)/(m1+m2)
        st.metric("Velocidade final (colisão perfeitamente inelástica)", f"{vf:.2f} m/s")
        st.info("Quantidade de movimento total é conservada.")
    elif sim == "Movimento Circular Uniforme":
        r=max(0.5,x/20); T=max(0.1,y/10); w=2*math.pi/T; v=w*r
        st.metric("Velocidade linear", f"{v:.2f} m/s"); st.metric("Aceleração centrípeta", f"{v*v/r:.2f} m/s²")
        st.info("No MCU, módulo da velocidade é constante e direção muda.")
    elif sim == "Gravitação Universal":
        m1=x*1e3; m2=y*1e3; r=1e3
        F=6.67e-11*m1*m2/r**2
        st.metric("Força gravitacional", f"{F:.2e} N")
        st.info("F = G m1 m2 / r².")
    elif sim == "Calorimetria e Equilíbrio Térmico":
        m1=max(1,x); T1=80; m2=max(1,y); T2=20; Te=(m1*T1+m2*T2)/(m1+m2)
        st.metric("Temperatura de equilíbrio", f"{Te:.2f} °C")
        st.info("Calor cedido = calor recebido (sistema isolado).")
    elif sim == "Dilatação Térmica":
        L0=max(1,x/10); dT=y-20; alpha=1.2e-5
        dL=L0*alpha*dT
        st.metric("Dilatação linear", f"{dL:.6f} m")
        st.info("Superficial ≈ 2α e volumétrica ≈ 3α para sólidos isotrópicos.")
    elif sim == "Transformações Gasosas":
        n=1; T=max(200,x+200); V=max(0.001,y/1000); P=n*R_GAS*T/V
        st.metric("Pressão (gás ideal)", f"{P:.2f} Pa")
        st.info("PV=nRT. Isotérmica: T cte; Isobárica: P cte; Isovolumétrica: V cte.")
    elif sim == "Ondas em Cordas":
        L=max(0.2,x/10); Tension=max(1,y); mu=0.01; v=math.sqrt(Tension/mu); f=v/(2*L)
        st.metric("Velocidade da onda", f"{v:.2f} m/s"); st.metric("Frequência fundamental", f"{f:.2f} Hz")
        st.info("f1 = v/(2L) em corda fixa nas extremidades.")
    elif sim == "Efeito Doppler":
        f0=max(100,x*10); vs=y/2; v=340; f=f0*(v/(v-vs))
        st.metric("Frequência observada (fonte se aproximando)", f"{f:.2f} Hz")
        st.info("A aproximação aumenta a frequência percebida.")
    elif sim == "Espelhos":
        f=(x-50)/2 or 1; p=max(1,y); q=1/(1/f-1/p) if f!=0 and (1/f-1/p)!=0 else float('inf')
        st.metric("Distância da imagem q", f"{q:.2f} cm")
        st.info("Equação dos espelhos: 1/f = 1/p + 1/q.")
    elif sim == "Lentes":
        f=(x-50)/2 or 1; p=max(1,y); q=1/(1/f-1/p) if f!=0 and (1/f-1/p)!=0 else float('inf')
        st.metric("Distância da imagem q", f"{q:.2f} cm")
        st.info("Equação das lentes delgadas: 1/f = 1/p + 1/q.")

    questoes([
        ("Qual grandeza principal deste simulador?", "Depende do tema selecionado."),
        ("O que ocorre ao aumentar o parâmetro 1?", "Observe o gráfico e a tendência física."),
        ("Qual lei/modelo foi aplicado?", "Ver interpretação física acima.")
    ])
