import streamlit as st
import random
import time
import os
import requests
import urllib3
import threading
from datetime import datetime

# --- CONFIGURACIÓN DE SEGURIDAD ---
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="¡NOTIFICACIÓN URGENTE! 🚨", page_icon="☀️")

WEBHOOK_URL = "https://script.google.com/macros/s/AKfycby2bBnnuC6B5UapN7KwhEZXvF4a7zKHPQ0IvQIU_RqYv7kBKSOX5P-UaQjKOtwH7PCmiw/exec"

def enviar_datos_hilo(accion, detalle):
    try:
        requests.post(WEBHOOK_URL, json={"accion": accion, "detalle": detalle}, timeout=10, verify=False)
    except:
        pass

def registrar_en_nube(accion, detalle):
    hilo = threading.Thread(target=enviar_datos_hilo, args=(accion, detalle))
    hilo.start()

# --- ESTADO DE LA SESIÓN ---
if 'contador' not in st.session_state:
    st.session_state.contador = 0
if 'mensaje_revelado' not in st.session_state:
    st.session_state.mensaje_revelado = False
if 'sesion_iniciada' not in st.session_state:
    registrar_en_nube("SISTEMA", "App abierta")
    st.session_state.sesion_iniciada = True

# --- DISEÑO VISUAL ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(-45deg, #e3f2fd, #fce4ec, #f3e5f5, #e8f5e9);
        background-size: 400% 400%;
        animation: gradient 20s ease infinite;
    }
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .stMarkdown, .stButton, .stSlider, .stRadio {
        background-color: rgba(255, 255, 255, 0.4);
        padding: 15px; border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.5);
    }
    .log-container {
        background-color: #1e1e1e; color: #d4d4d4;
        font-family: 'Courier New', Courier, monospace;
        padding: 12px; border-radius: 10px;
        border-left: 5px solid #007acc; margin: 10px 0; font-size: 0.85em;
    }
    .log-time { color: #569cd6; }
    .floating-icon {
        position: fixed; bottom: -50px; font-size: 40px;
        animation: floatUp 3s ease-in forwards; z-index: 9999;
    }
    @keyframes floatUp {
        0% { transform: translateY(0); opacity: 1; }
        100% { transform: translateY(-80vh); opacity: 0; }
    }
    </style>
    """, unsafe_allow_html=True)

def print_log_visual(mensaje, tipo="INFO"):
    ahora = datetime.now().strftime("%H:%M:%S")
    st.markdown(f'<div class="log-container"><span class="log-time">[{ahora}]</span> [{tipo}] {mensaje}</div>', unsafe_allow_html=True)

def lanzar_efecto(tipo="besos"):
    iconos = ["💋", "❤️", "😘"] if tipo == "besos" else ["✨", "🎉", "🌈"]
    html_content = "".join([f'<div class="floating-icon" style="left:{random.randint(5, 95)}vw; animation-delay:{random.uniform(0, 1)}s;">{random.choice(iconos)}</div>' for _ in range(15)])
    area = st.empty()
    area.markdown(html_content, unsafe_allow_html=True)
    time.sleep(1.5)
    area.empty()

def typewriter(text, speed=0.10):
    container = st.empty()
    full_text = ""
    for word in text.split(" "):
        full_text += word + " "
        container.markdown(full_text + "▌")
        time.sleep(speed)
    container.markdown(full_text)

# --- CONTENIDO PRINCIPAL ---
st.title("¡Buenos días! ☀️😊")

if os.path.exists("Cuentame.mp3"):
    st.audio("Cuentame.mp3", format="audio/mp3")

st.write("Intento programar, lo hice con ayuda de la IA ¡Este proyecto va para ti!.. pero seguro aprenderé más! 🙃")
st.write("---")

# Slider con opción inicial "vacía"
nivel_abrazo = st.select_slider('**¿Qué tan fuerte necesitas el apapacho hoy?**', 
                                options=['Desliza aquí... ➡️', 'Suavecito ☁️', 'Normal 😊', 'Oso polar 🐻', 'Rompe-costillas ❤️'])

# Solo mostramos el contenido si eligió algo distinto a la opción inicial
if nivel_abrazo != 'Desliza aquí... ➡️':
    zoom_levels = {
        'Suavecito ☁️': ('☁️', '80px', 'suavecito.gif'),
        'Normal 😊': ('😊', '110px', 'normal.gif'),
        'Oso polar 🐻': ('🧸', '140px', 'osopolar.gif'),
        'Rompe-costillas ❤️': ('🫂', '180px', 'abrazorompecostilla.gif')
    }
    emoji, size, archivo_gif = zoom_levels[nivel_abrazo]

    st.markdown(f'<div style="text-align:center; font-size:{size}; margin:10px 0;">{emoji}</div>', unsafe_allow_html=True)

    if os.path.exists(archivo_gif):
        col_img = st.columns([1, 2, 1])[1]
        with col_img:
            st.image(archivo_gif, use_container_width=True)
else:
    st.info("Desliza el control de arriba para recibir tu abrazo... 🫂")

# Pregunta
st.write("---")
opcion = st.radio("¿Por qué crees que hice esto para ti?", 
                  ["Selecciona una opción...", "Porque estás loquita", "Porque soy increíble", "Porque me extrañas"], index=0)

if opcion != "Selecciona una opción...":
    registrar_en_nube("PREGUNTA", f"Respuesta: {opcion}")
    print_log_visual("Procesando nivel de cariño...", "SUCCESS")
    if opcion == "Porque estás loquita": st.success("¡Bingo! Una locura de las buenas. 🤪")
    elif opcion == "Porque soy increíble": st.info("Exacto. Eres fenomenal. ✨")
    elif opcion == "Porque me extrañas": st.write("Bueno... en el fondo sabes que sí, y mucho. 🥺❤️")
    st.toast("Me atrapaste... 🫣")
    
# Manifiesto
st.write("---")
with st.expander("HAZ CLIC PARA EL MANIFIESTO DE MI CORAZÓN 💌"):
    mensaje = """### ¡Holitas! Una bonita mañana al despertar... ☀️\nQue Dios te proteja y te bendiga. Hoy deseo que te recargues de toda esa energía carismática y auténtica; esa misma que transmites a través de tus ojos y que llevas contigo a donde vas. 

Que hoy el cafelito te sepa delicioso y que tu sonrisa sea quien ilumine el día. Y no importa que esté a kilómetros, ten por seguro que una parte de mi corazón está contigo deseándote todo lo hermoso. 😊

**Desayuna bien.** Estaré dormida cuando lo leas, quizás te robe una sonrisa, pero te dejo un abrazo de esos que apapachan el alma. ¡Así que vamos con toda hoy! 😋. 

Que pases un dia genial🤗🤗🤗🤍🤍❤️🥰

¡Te quiero mucho Ches! ❤️😘😘"""
    
    if not st.session_state.mensaje_revelado:
        if st.button("Leer mensaje poco a poco... ✨"):
            registrar_en_nube("MANIFIESTO", "Revelado")
            st.session_state.mensaje_revelado = True
            typewriter(mensaje)
            st.rerun()
    else:
        st.markdown(mensaje)

# Besos
st.write("---")
col_b1, col_b2 = st.columns([1, 1])
with col_b1:
    if st.button("¡Enviar 3 besos de golpe! 💋💋💋"):
        st.session_state.contador += 3 # Ahora sí suma de 3 en 3
        registrar_en_nube("BESOS", f"Total: {st.session_state.contador}")
        print_log_visual("Enviando ráfaga de besos...", "SUCCESS")
        lanzar_efecto("besos")
        st.toast("¡Muuua! ❤️")
with col_b2:
    st.metric("Besos acumulados", st.session_state.contador)

# Final
if st.button("Finalizar con un abrazo virtual 🫂"):
    registrar_en_nube("FINAL", f"Cerró con {st.session_state.contador} besos")
    lanzar_efecto("fiesta")
    st.balloons()
    print_log_visual("Sincronización de afecto completada.", "SUCCESS")
    st.write("### ¡A comerse el mundo hoy! Te quiero. ❤️")
