from importlib.resources import files

import streamlit as st
from pathlib import Path

# ==========================================================
# 0) CONFIG + CSS
# ==========================================================
st.set_page_config(
    page_title="Yamaha | Demo Marina",
    page_icon="🛥️",
    layout="wide",
)

def load_css(file_name: str = "styles.css"):
    css_path = Path(__file__).parent / file_name
    if css_path.exists():
        st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)
    else:
        st.warning(f"No se encontró {file_name}. Crea el archivo en la misma carpeta de app.py.")

load_css("styles.css")


# ==========================================================
# 1) CONSTANTES (Stepper + Lists)
# ==========================================================
MENU = [
    "Solicitar crédito",
    "Estudio crédito",
    "Formalización",
    "Pendientes",
    "Finalización",
]

# Stepper horizontal (con lanchas). Paso 1 y Paso 2 reales, resto demo.
STEP_MODELS = [
    {"key": "p1", "title": "Paso 1", "desc": "Conocimiento del cliente", "icon": "boatSvg"},
    {"key": "p2", "title": "Paso 2", "desc": "Documentación", "icon": "boatSvg2"},
    {"key": "p3", "title": "Paso 3", "desc": "Estudio", "icon": "boatSvg"},
    {"key": "p4", "title": "Paso 4", "desc": "Formalización", "icon": "boatSvg2"},
    {"key": "p5", "title": "Paso 5", "desc": "Finalización", "icon": "boatSvg"},
]

DOC_TYPES = ["CC", "CE", "NIT", "PAS", "TI"]
ENTITY_TYPES = ["Pública", "Privada", "Mixta"]
SI_NO = ["SI", "NO"]
REGIMEN = ["Común", "Simplificado"]
TIPO_CUENTA = ["Ahorros", "Corriente"]

PRODUCTOS = ["Wholesale", "Retail"]
MODALIDADES = ["Marina", "Motocicletas", "Instrumentos Musicales", "Repuestos"]


# ==========================================================
# 2) SESSION STATE (datos base)
# ==========================================================
def init_state():
    if "step" not in st.session_state:
        st.session_state.step = 0  # 0 = Paso 1

    # Estado de completitud del Paso 1 (para habilitar Paso 2)
    if "p1_ready" not in st.session_state:
        st.session_state.p1_ready = False

    # Datos KYC (mock / quemados) — basados en tu Word, con defaults solicitados:
    # - Producto: Wholesale (predeterminado)
    # - Modalidad: Marina (predeterminado)
    # - Sin campos de fecha en el primer acordeón
    if "kyc" not in st.session_state:
        st.session_state.kyc = {
            # Encabezado (sin fecha)
            "tipo_solicitud": "Creación",
            "producto": "Wholesale",
            "modalidad": "Marina",
            "tipo_activo": "Motor fuera de borda",
            "uso_activo": "Comercial (pesca, turismo, transporte)",
            "zona_operacion": "Costa",

            # Uso exclusivo (opcional)
            "zona_matricular": "",
            "coordinador_zonal": "",

            # Datos generales
            "razon_social": "Empresa Demo S.A.S",
            "nit_sin_dv": "900123456",
            "tipo_entidad": "Privada",
            "obligado_sagrilaft": "NO",

            # Información comercial
            "actividad_economica": "Comercio al por menor",
            "ciiu_principal": "4771",
            "ciiu_otros": "",

            # Información de contacto
            "direccion_principal": "Calle 00 #00-00",
            "ciudad": "Medellín",
            "departamento": "Antioquia",
            "pais": "Colombia",
            "pagina_web": "https://www.ejemplo.com",
            "nombre_contacto_principal": "Contacto Demo",
            "cargo_contacto": "Administrador",
            "telefono_contacto": "6040000000",
            "celular_contacto": "3000000000",
            "email_contacto": "contacto@ejemplo.com",
            "tel_area_contable": "6041111111",
            "tel_area_tesoreria": "6042222222",
            "email_cert_tributarios": "tributario@ejemplo.com",
            "email_soportes_pago": "pagos@ejemplo.com",
            "email_fact_electronica": "facturacion@ejemplo.com",

            # Representante legal
            "rep_nombre": "Representante Demo",
            "rep_tipo_id": "CC",
            "rep_numero": "1020304050",
            "rep_telefono": "6043333333",
            "rep_celular": "3011111111",
            "rep_email": "rep@ejemplo.com",

            # Preguntas PEP
            "rep_pep": "NO",
            "rep_reconocimiento": "NO",
            "rep_recursos_publicos": "NO",
            "rep_vinculo_pep": "NO",
            "rep_especificacion": "",

            # Tributaria
            "regimen": "Común",
            "gran_contribuyente": "NO",
            "num_resolucion_gc": "",
            "calidad_iva": "",
            "agente_retencion_fuente": "NO",
            "sujeta_retencion_fuente": "NO",
            "autorretenedor_renta": "NO",
            "responsable_ica": "NO",
            "ciudades_ica": "",
            "autorretenedor_ica": "NO",
            "resolucion_ica_fecha": "",

            # Bancaria
            "entidad_bancaria": "Bancolombia",
            "num_cuenta": "1234567890",
            "tipo_cuenta": "Ahorros",

            # Financiera
            "ing_operacionales": 1500,
            "ing_no_operacionales": 50,
            "egresos": 900,
            "activo_corriente": 700,
            "total_activo": 1300,
            "pasivo_corriente": 400,
            "total_pasivo": 600,
            "patrimonio": 700,
            "detalle_ing_no_op": "Intereses / Otros",

            # Internacionales
            "trx_moneda_extranjera": "NO",
            "cual_moneda": "",
            "prod_fin_exterior": "NO",
            "cuentas_moneda_extranjera": "NO",
            "tipo_producto_exterior": "",

            # T&C (SIN OTP / SIN SIMULACIÓN)
            "acepta_tratamiento_datos": False,
            "acepta_tyc": False,
        }

    # Tabla composición accionaria (modo claro)
    if "accionistas" not in st.session_state:
        st.session_state.accionistas = [
            {"Tipo de ID": "CC", "Número": "1000000001", "Nombre y Apellidos": "Accionista 1", "% Participación": 60, "¿PEP?": "NO"},
            {"Tipo de ID": "CC", "Número": "1000000002", "Nombre y Apellidos": "Accionista 2", "% Participación": 40, "¿PEP?": "NO"},
        ]

    if "page" not in st.session_state:
        st.session_state.page = "Solicitar crédito"

    if "show_submit_modal" not in st.session_state:
        st.session_state.show_submit_modal = False

    if "docs_uploaded" not in st.session_state:
        st.session_state.docs_uploaded = False

    if "page" not in st.session_state:
        st.session_state.page = "Solicitar crédito"

    # =========================
    # Estado del estudio de crédito (DEMO)
    # =========================
    if "study" not in st.session_state:
        st.session_state.study = {
            "estado": "En estudio",                  # En estudio / Decidido
            "radicado": "SOL-2026-000123",           # ficticio
            "buro": "OK",                            # OK / Alerta
            "listas": "OK",                          # OK / Coincidencia
            # OJO: NO usamos Validación identidad (por tu proceso)
            "score_buro": 712,                       # ficticio
            "icp": 1.8,                              # ficticio (Balance/Cuota)
            "endeudamiento": "Medio",                # Bajo/Medio/Alto
            "uso_activo": "Comercial",               # Comercial/Recreativo
            "zona": "Costa",                         # Costa/Río/Lago
            "estacionalidad": "Media",               # Alta/Media/Baja
            "formalidad": "Media",                   # Alta/Media/Baja
            "verificacion_activo": "Verificado",     # Verificado/Pendiente
            "decision": None,                        # Aprobado/Congelado/Rechazado
            "causal_rechazo": "Score insuficiente",  # demo
            "motivo_congelado": "Falta documentación",# demo
    
        }

    
    if "final" not in st.session_state:
        st.session_state.final = {
            "formalizacion_ok": False,
            "seguros_ok": False,
            "garantias_ok": False,
        }

    if "pendientes" not in st.session_state:
        st.session_state.pendientes = [
            {"item": "Documento adicional: evidencia de ingresos del activo", "estado": "Pendiente"},
            {"item": "Validación de actividad económica (llamada)", "estado": "Pendiente"},
            {"item": "Validación del activo/proveedor", "estado": "Pendiente"},
        ]

    # Aplicar navegación pendiente de step (si existe)
    if "pending_step" in st.session_state and st.session_state.pending_step is not None:
        st.session_state.step = st.session_state.pending_step
        st.session_state.pending_step = None

    

init_state()


# ==========================================================
# 3) UI: SIDEBAR + HERO
# ==========================================================
with st.sidebar:
    st.markdown("### Panel de administración")

    # 1) defaults
    if "page" not in st.session_state:
        st.session_state.page = "Solicitar crédito"

    if "menu_choice" not in st.session_state:
        st.session_state.menu_choice = st.session_state.page

    if "pending_page" not in st.session_state:
        st.session_state.pending_page = None

    # 2) aplicar navegación pendiente ANTES de crear el widget
    if st.session_state.pending_page:
        st.session_state.page = st.session_state.pending_page
        st.session_state.menu_choice = st.session_state.pending_page
        st.session_state.pending_page = None

    # 3) crear radio (el usuario ya puede cambiarlo)
    choice = st.radio(
        "Menú",
        MENU,
        index=MENU.index(st.session_state.menu_choice) if st.session_state.menu_choice in MENU else 0,
        key="menu_choice",
        label_visibility="collapsed"
    )

    # 4) sincronizar page con lo que el usuario eligió
    st.session_state.page = choice

    st.divider()
    st.caption("Yamaha Servicios Financieros · Confía en quien mejor te conoce.")


# st.markdown(
#     """
#     <div class="hero">
#       <div>
#         <div class="title">YAMAHA</div>
#         <div class="subtitle">Servicios Financieros · Confía en quien mejor te conoce.</div>
#       </div>
#       <div class="badge">DEMO</div>
#     </div>
#     """,
#     unsafe_allow_html=True
# )

import base64

def img_to_base64(path: str) -> str:
    p = Path(__file__).parent / path
    if not p.exists():
        return ""
    return base64.b64encode(p.read_bytes()).decode("utf-8")

y_logo = img_to_base64("assets/yamaha.png")
a_logo = img_to_base64("assets/aliado.png")  # <-- tu segundo logo

logos_html = ""
if y_logo and a_logo:
    logos_html = f"""
      <div class="hero-logos">
        <img src="data:image/png;base64,{y_logo}" alt="Yamaha logo">
        <div class="divider"></div>
        <img src="data:image/png;base64,{a_logo}" alt="Logo aliado">
      </div>
    """
elif y_logo:
    logos_html = f"""
      <div class="hero-logos">
        <img src="data:image/png;base64,{y_logo}" alt="Yamaha logo">
      </div>
    """

st.markdown(
    f"""
    <div class="hero">
      <div>
        {logos_html}
      </div>
      <div class="badge">DEMO</div>
    </div>
    """,
    unsafe_allow_html=True
)


# ==========================================================
# 4) STEPPER HORIZONTAL (INTERACTIVO con lanchas)
# ==========================================================
def step_state(idx: int, active_idx: int) -> str:
    """Retorna: done | active | normal"""
    if idx < active_idx:
        return "done"
    if idx == active_idx:
        return "active"
    return "normal"

def can_go_to_step(target_idx: int) -> bool:
    """
    Reglas de navegación:
    - Siempre puedes ir al paso actual o anteriores.
    - Solo puedes ir al Paso 2 si Paso 1 está listo (p1_ready).
    - Pasos >2 quedan bloqueados (demo) por ahora.
    """
    current = st.session_state.step
    if target_idx <= current:
        return True
    if target_idx == 1:
        return bool(st.session_state.p1_ready)
    return False

def render_stepper(active_idx: int):
    st.markdown('<div class="stepper-wrap">', unsafe_allow_html=True)

    # Mantener columnas: asegura que queden uno al lado del otro
    cols = st.columns(len(STEP_MODELS), gap="small")

    for i, step in enumerate(STEP_MODELS):
        state = step_state(i, active_idx)

        cls = "stepCard"
        if state == "active":
            cls += " active"
        elif state == "done":
            cls += " done"

        with cols[i]:
            # Solo el cuadrito/card (sin botón "Ir")
            st.markdown(
                f"""
                <div class="{cls}">
                  <div class="stepIcon"><span class="{step['icon']}"></span></div>
                  <div class="stepTxt">
                    <div class="stepTitle">{step['title']}</div>
                    <div class="stepDesc">{step['desc']}</div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("</div>", unsafe_allow_html=True)


# Si estoy en Estudio, resaltar Paso 3 (index 2)

if st.session_state.page == "Estudio crédito":
    active_idx = 2  # Paso 3
elif st.session_state.page == "Formalización":
    active_idx = 3  # Paso 4 ✅
elif st.session_state.page == "Pendientes":
    active_idx = 2  # sigue en Estudio (Paso 3) aunque esté congelado
elif st.session_state.page == "Finalización":
    active_idx = 4  # Paso 5 (Finalización)
elif st.session_state.page == "Solicitar crédito":
    # Paso 1 y 2 dependen de step: 0->Paso1, 1->Paso2
    active_idx = st.session_state.step
else:
    active_idx = 0


render_stepper(active_idx)


# ==========================================================
# 5) HELPERS para Cards
# ==========================================================
def card_open(title: str, subtitle: str = ""):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f'<div class="form-h">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="form-p">{subtitle}</div>', unsafe_allow_html=True)

def card_close():
    st.markdown("</div>", unsafe_allow_html=True)

def kyc():
    return st.session_state.kyc


def go(page: str, step=None):
    """Navegación segura: NO modifica el estado del radio después de creado."""
    st.session_state.pending_page = page
    if step is not None:
        st.session_state.pending_step = step
    st.rerun()

@st.dialog("✅ Solicitud radicada")
def submit_dialog():
    st.write("Tu solicitud pasará a **Estudio de crédito**.")
    st.write("En la demo podrás ver cómo se evaluaría el caso con ejemplos ficticios.")

    c1, c2 = st.columns([2, 1])

    with c1:
        if st.button("Ir a Estudio de crédito", use_container_width=True, key="dialog_go_study"):
            st.session_state.show_submit_modal = False
            go("Estudio crédito")

    with c2:
        if st.button("Cerrar", use_container_width=True, key="dialog_close"):
            st.session_state.show_submit_modal = False
            st.rerun()

# ==========================================================
# 6) RUTEO (en Parte 2 implementamos contenido real de Paso 1 y Paso 2)
# ==========================================================
def render_placeholder(title: str, msg: str):
    card_open(title, "")
    st.info(msg)
    card_close()

def render_estudio_credito():
    card_open("📊 Estudio de crédito", "Simulación demo con tarjetas + decisión manual del analista (sin backend).")

    study = st.session_state.study
    data = st.session_state.kyc  # usamos datos reales del Paso 1 (razón social, nit, etc.)

    # =========================
    # 1) Encabezado de caso
    # =========================
    c1, c2, c3, c4 = st.columns([1.2, 1.2, 1.2, 1.2])
    with c1:
        st.metric("Radicado", study["radicado"])
    with c2:
        st.metric("Estado", study["estado"])
    with c3:
        st.metric("Producto", data.get("producto", "Wholesale"))
    with c4:
        st.metric("Modalidad", data.get("modalidad", "Marina"))


    # =========================
    # 2) Validaciones automáticas (SIN identidad)
    #    Doc base: Buró + Listas como automáticas. 【1-785c2e】
    # =========================
    st.markdown("### Validaciones automáticas (DEMO)")
    v1, v2 = st.columns(2)
    with v1:
        st.markdown("**Buró de crédito (Experian)**")  # demo
        st.selectbox("Resultado", ["OK", "Alerta"], index=["OK", "Alerta"].index(study["buro"]), key="study_buro")
        study["buro"] = st.session_state.study_buro
    with v2:
        st.markdown("**Listas restrictivas (SARLAFT)**")  # demo
        st.selectbox("Resultado", ["OK", "Coincidencia"], index=["OK", "Coincidencia"].index(study["listas"]), key="study_listas")
        study["listas"] = st.session_state.study_listas

    # st.divider()

    # =========================
    # 3) Scoring + capacidad de pago (tarjetas)
    #    Doc: score buró + score capacidad pago + evaluación financiera (ICP). 【1-785c2e】
    # =========================
    st.markdown("### Scoring y capacidad de pago (DEMO)")
    s1, s2, s3 = st.columns(3)
    with s1:
        st.metric("Score buró", f"{study['score_buro']}")
    with s2:
        st.metric("ICP (Balance/Cuota)", f"{study['icp']}")
    with s3:
        st.metric("Endeudamiento", study["endeudamiento"])

    # st.divider()

    # =========================
    # 4) Evaluación especializada Marino (diferenciadores)
    #    Doc: uso activo, zona, estacionalidad, formalidad, verificación activo. 【1-785c2e】
    # =========================
    st.markdown("### Evaluación especializada (Marina) — DEMO")

    e1, e2, e3 = st.columns(3)
    with e1:
        study["uso_activo"] = st.selectbox("Uso del activo", ["Comercial", "Recreativo"],
                                           index=["Comercial", "Recreativo"].index(study["uso_activo"]))
    with e2:
        study["zona"] = st.selectbox("Zona de operación", ["Costa", "Río", "Lago"],
                                     index=["Costa", "Río", "Lago"].index(study["zona"]))
    with e3:
        study["estacionalidad"] = st.selectbox("Estacionalidad", ["Alta", "Media", "Baja"],
                                               index=["Alta", "Media", "Baja"].index(study["estacionalidad"]))

    e4, e5 = st.columns(2)
    with e4:
        study["formalidad"] = st.selectbox("Formalidad del negocio", ["Alta", "Media", "Baja"],
                                           index=["Alta", "Media", "Baja"].index(study["formalidad"]))
    with e5:
        study["verificacion_activo"] = st.selectbox("Verificación del activo/proveedor", ["Verificado", "Pendiente"],
                                                    index=["Verificado", "Pendiente"].index(study["verificacion_activo"]))

    # Zona de análisis (toggle demo)
    st.markdown("#### Zona de análisis (DEMO)")
    zona_analisis = st.toggle("Activar Zona de análisis (cuando no pasa automático)", value=False)

    if zona_analisis:
        st.info("Zona de análisis activa: se solicitarían documentos adicionales / visita / referenciación (DEMO).")
        za1, za2, za3 = st.columns(3)
        with za1:
            st.checkbox("Solicitar documentos adicionales", value=True)
        with za2:
            st.checkbox("Programar visita en sitio", value=True)
        with za3:
            st.checkbox("Referenciación telefónica", value=True)

    # st.divider()

    # =========================
    # 5) Decisión interactiva (tu elección 🅑)
    #    Doc: Aprobado / Congelado / Rechazado y causales. 【1-785c2e】
    # =========================
    st.markdown("### Decisión del analista (DEMO)")

    d1, d2, d3 = st.columns(3)
    with d1:
        if st.button("✅ Aprobar", use_container_width=True):
            study["decision"] = "Aprobado"
            study["estado"] = "Decidido"
            st.toast("Decisión registrada: Aprobado", icon="✅")
    with d2:
        if st.button("⏸️ Congelar", use_container_width=True):
            study["decision"] = "Congelado"
            study["estado"] = "Decidido"
            st.toast("Decisión registrada: Congelado", icon="⏸️")
    with d3:
        if st.button("❌ Rechazar", use_container_width=True):
            study["decision"] = "Rechazado"
            study["estado"] = "Decidido"
            st.toast("Decisión registrada: Rechazado", icon="❌")

    # Resultado visible
    if study["decision"]:
        st.markdown("#### Resultado del estudio")
        if study["decision"] == "Aprobado":
            st.success("✅ Aprobado (DEMO): pasaría a Formalización (seguros + garantías).")
        elif study["decision"] == "Congelado":
            study["motivo_congelado"] = st.selectbox(
                "Motivo de congelación (DEMO)",
                ["Falta documentación", "Validación de actividad", "Validación del activo"],
                index=["Falta documentación", "Validación de actividad", "Validación del activo"].index(study["motivo_congelado"])
            )
            st.warning(f"⏸️ Congelado (DEMO): {study['motivo_congelado']}")
        else:
            study["causal_rechazo"] = st.selectbox(
                "Causal de rechazo (DEMO)",
                ["No demuestra ingresos", "Alto endeudamiento", "Actividad no verificable", "Score insuficiente"],
                index=["No demuestra ingresos", "Alto endeudamiento", "Actividad no verificable", "Score insuficiente"].index(study["causal_rechazo"])
            )
            st.error(f"❌ Rechazado (DEMO): {study['causal_rechazo']}")
        
        if study["decision"] == "Aprobado":
            if st.button("Ir a Formalización →", use_container_width=True):
                go("Formalización")

        elif study["decision"] == "Congelado":
            if st.button("Ver Pendientes →", use_container_width=True):
                go("Pendientes")

        elif study["decision"] == "Rechazado":
            if st.button("Ver Resultado →", use_container_width=True):
                go("Finalización")

def render_pendientes_congelado():
    card_open("Pendientes de Estudio (DEMO)", "Tu solicitud quedó congelada por información pendiente. (Vista demo)")

    st.warning("Estado: Congelado — se requiere completar validaciones o documentos antes de decidir. ")

    st.markdown("### Pendientes")
    # tabla editable demo (modo claro)
    st.session_state.pendientes = st.data_editor(
        st.session_state.pendientes,
        use_container_width=True,
        num_rows="dynamic",
        column_config={
            "estado": st.column_config.SelectboxColumn(options=["Pendiente", "En revisión", "Completado"])
        }
    )

    st.markdown("### Acción")
    c1, c2 = st.columns([2, 1])
    with c1:
        st.caption("En un flujo real, aquí se solicitarían documentos/visita/referenciación según la política. ")
    with c2:
        # Ir a Paso 2 (Documentación)
        if st.button("Ir a Documentación (Paso 2) →", use_container_width=True):
            st.session_state.page = "Solicitar crédito"
            st.session_state.step = 1
            st.rerun()
    
    card_close()

def render_formalizacion():
    card_open("✅ Paso 4 | Formalización (DEMO)", "Documentos + Seguros + Garantías (en un solo paso).")

    st.info("Esta pantalla simula la formalización posterior a una decisión Aprobada. ")

    f = st.session_state.final
    study = st.session_state.study

    st.markdown("### Documentos")
    f["formalizacion_ok"] = st.checkbox("Carta de aprobación / Pagaré / Contrato (DEMO)", value=f["formalizacion_ok"])

    st.markdown("### Seguros (crítico en marino)")
    f["seguros_ok"] = st.checkbox("Seguro de vida + Seguro del bien (todo riesgo obligatorio) (DEMO)", value=f["seguros_ok"])  # 

    st.markdown("### Garantías (DEMO)")
    f["garantias_ok"] = st.checkbox("Garantía/prenda sobre el activo (motor/bote/moto acuática) o alternativa (DEMO)", value=f["garantias_ok"])  # 

    # st.divider()

    listo = f["formalizacion_ok"] and f["seguros_ok"] and f["garantias_ok"]

    c1, c2 = st.columns([3, 1])
    with c1:
        if listo:
            st.success("Formalización completa (DEMO). Ya puedes ver el resultado final.")
        else:
            st.warning("⚠️ Marca los 3 checks para finalizar la formalización (DEMO).")

    with c2:
        if st.button("Finalizar →", disabled=not listo, use_container_width=True):
            if study.get("decision") == "Aprobado":
                f["finalizado"] = True
                go("Finalización")

    card_close()

def render_resultado():
    card_open("Finalización", "Resumen final según la decisión del estudio.")

    study = st.session_state.study
    decision = study.get("decision")

    if not decision:
        st.info("Aún no hay decisión. Ve a 📊 Estudio de crédito y selecciona Aprobar / Congelar / Rechazar.")
        card_close()
        return

    if decision == "Aprobado":
        st.success("✅ Crédito Aprobado (DEMO). Continuó a formalización con seguros y garantías. ")
        st.markdown("- Estado: **Aprobado**")
        st.markdown("- Siguiente: **Formalización completada** (DEMO)")
    elif decision == "Congelado":
        st.warning("⏸️ Solicitud Congelada (DEMO). Debe completarse documentación/validaciones. ")
        st.markdown(f"- Motivo: **{study.get('motivo_congelado', 'Falta documentación')}**")
    else:
        st.error("❌ Crédito Rechazado (DEMO). ")
        st.markdown(f"- Causal: **{study.get('causal_rechazo', 'Score insuficiente')}**")

    st.divider()
    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button("Volver a Estudio", use_container_width=True):
            st.session_state.page = "Estudio crédito"
            st.rerun()
    with c2:
        if st.button("Volver a Solicitud", use_container_width=True):
            st.session_state.page = "Solicitar crédito"
            st.session_state.step = 0
            st.rerun()

    card_close()

def render_finalizacion():
    card_open("📩 Paso 5 | Finalización", "Resumen final del proceso y estado de la solicitud.")

    study = st.session_state.study
    data = st.session_state.kyc
    final = st.session_state.final

    decision = study.get("decision")
    formalizado = final.get("finalizado", False)

    # =========================
    # 1) Resumen superior en cards
    # =========================
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Radicado", study.get("radicado", "SOL-2026-000123"))
    with c2:
        st.metric("Producto", data.get("producto", "Wholesale"))
    with c3:
        st.metric("Modalidad", data.get("modalidad", "Marina"))
    with c4:
        if decision == "Aprobado" and formalizado:
            st.metric("Estado final", "Formalizado")
        elif decision == "Aprobado":
            st.metric("Estado final", "Aprobado")
        elif decision == "Congelado":
            st.metric("Estado final", "Congelado")
        elif decision == "Rechazado":
            st.metric("Estado final", "Rechazado")
        else:
            st.metric("Estado final", "Sin decisión")

    # =========================
    # 2) Tarjeta central según decisión
    # =========================
    if not decision:
        st.info("Aún no hay decisión registrada. Ve a Estudio y selecciona Aprobado / Congelado / Rechazado.")
        card_close()
        return

    if decision == "Aprobado":
        if formalizado:
            st.success("✅ Solicitud aprobada y formalizada")
        else:
            st.success("✅ Solicitud aprobada")

        st.markdown("### Resumen")
        st.markdown("- Estado de estudio: **Aprobado**")

        if formalizado:
            st.markdown("- Formalización: **Completada**")
            st.markdown("- Resultado final: **Solicitud finalizada correctamente**")
        else:
            st.markdown("- Formalización: **Pendiente**")
            st.markdown("- Resultado final: **Aprobada pendiente por formalización**")

        # Tarjeta simple
        if formalizado:
            st.markdown(
                """
                <div class="card" style="border-left: 6px solid #10B981;">
                <div class="form-h" style="margin-bottom:8px;">✅ Aprobado y formalizado</div>
                <div class="form-p">
                    La solicitud fue aprobada correctamente y completó la formalización.
                </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <div class="card" style="border-left: 6px solid #10B981;">
                <div class="form-h" style="margin-bottom:8px;">✅ Aprobado</div>
                <div class="form-p">
                    La solicitud fue aprobada correctamente, pero aún no completa la formalización.
                </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    elif decision == "Congelado":
        motivo = study.get("motivo_congelado", "Falta documentación")

        st.warning("⏸️ Solicitud congelada")

        st.markdown("### Resumen")
        st.markdown("- Estado de estudio: **Congelado**")
        st.markdown(f"- Motivo: **{motivo}**")
        st.markdown("- Resultado final: **Pendiente por completar información o validaciones**")

        st.markdown(
            f"""
            <div class="card" style="border-left: 6px solid #F59E0B;">
              <div class="form-h" style="margin-bottom:8px;">⏸️ Congelado</div>
              <div class="form-p">
                La solicitud requiere gestión adicional antes de continuar.<br/>
                Motivo principal: <b>{motivo}</b>
              </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:  # Rechazado
        causal = study.get("causal_rechazo", "Score insuficiente")

        st.error("❌ Solicitud rechazada")

        st.markdown("### Resumen")
        st.markdown("- Estado de estudio: **Rechazado**")
        st.markdown(f"- Causal: **{causal}**")
        st.markdown("- Resultado final: **Solicitud no aprobada**")

        st.markdown(
            f"""
            <div class="card" style="border-left: 6px solid #EF4444;">
              <div class="form-h" style="margin-bottom:8px;">❌ Rechazado</div>
              <div class="form-p">
                La solicitud no fue aprobada.<br/>
                Causal principal: <b>{causal}</b>
              </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # =========================
    # 3) Botones de navegación
    # =========================
    b1, b2, b3 = st.columns(3)

    with b1:
        if st.button("Volver a Estudio", use_container_width=True):
            go("Estudio crédito")

    with b2:
        if st.button("Ir a Solicitud", use_container_width=True):
            go("Solicitar crédito", step=0)

    with b3:
        if decision == "Aprobado" and not formalizado:
            if st.button("Ir a Formalización", use_container_width=True):
                go("Formalización")
        elif decision == "Congelado":
            if st.button("Ir a Documentación", use_container_width=True):
                go("Solicitar crédito", step=1)
        elif decision == "Rechazado":
            st.button("Sin acción adicional", disabled=True, use_container_width=True)

    card_close()

# ==========================================================
# 7) PASO 1: Acordeones KYC + 2 checks + botón Continuar (derecha)
# ==========================================================
def paso_1():
    card_open(
        "Paso 1 | Conocimiento del cliente",
        "Completa la información por secciones. Al final acepta Tratamiento de Datos y T&C para habilitar Continuar al Paso 2."
    )

    # -------------------------
    # Encabezado (SIN FECHA)
    # -------------------------
    with st.expander("Encabezado de Solicitud (Tipo, Producto, Modalidad)", expanded=True):
        c1, c2, c3 = st.columns(3)
       
        with c1:
            kyc()["tipo_solicitud"] = st.selectbox(
                "Tipo de Solicitud",
                ["Creación", "Actualización"],
                index=["Creación", "Actualización"].index(kyc()["tipo_solicitud"])
            )

        with c2:
            default_prod = PRODUCTOS.index(kyc()["producto"]) if kyc()["producto"] in PRODUCTOS else 0
            kyc()["producto"] = st.selectbox("Producto", PRODUCTOS, index=default_prod)

        with c3:
            default_mod = MODALIDADES.index(kyc()["modalidad"]) if kyc()["modalidad"] in MODALIDADES else 0
            kyc()["modalidad"] = st.selectbox("Modalidad", MODALIDADES, index=default_mod)

        # Fila 2 - Campos marino
        c4, c5, c6 = st.columns(3)

        with c4:
            opciones_tipo_activo = ["Motor fuera de borda", "Bote", "Moto acuática"]
            current_tipo = kyc().get("tipo_activo", opciones_tipo_activo[0])
            kyc()["tipo_activo"] = st.selectbox(
                "Tipo de activo",
                opciones_tipo_activo,
                index=opciones_tipo_activo.index(current_tipo) if current_tipo in opciones_tipo_activo else 0
            )

        with c5:
            opciones_uso = ["Comercial (pesca, turismo, transporte)", "Recreativo"]
            current_uso = kyc().get("uso_activo", opciones_uso[0])
            kyc()["uso_activo"] = st.selectbox(
                "Uso del activo",
                opciones_uso,
                index=opciones_uso.index(current_uso) if current_uso in opciones_uso else 0
            )

        with c6:
            opciones_zona = ["Costa", "Río", "Lago"]
            current_zona = kyc().get("zona_operacion", opciones_zona[0])
            kyc()["zona_operacion"] = st.selectbox(
                "Zona de operación",
                opciones_zona,
                index=opciones_zona.index(current_zona) if current_zona in opciones_zona else 0
            )


    # -------------------------
    # Uso exclusivo Yamaha (opcional)
    # -------------------------
    with st.expander("Uso exclusivo Yamaha (Zona a matricular / Coordinador zonal)", expanded=False):
        c1, c2 = st.columns(2)
        with c1:
            kyc()["zona_matricular"] = st.text_input("Zona a Matricular", kyc()["zona_matricular"])
        with c2:
            kyc()["coordinador_zonal"] = st.text_input("Coordinador Zonal", kyc()["coordinador_zonal"])

    # -------------------------
    # Datos generales
    # -------------------------
    with st.expander("Datos generales", expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            kyc()["razon_social"] = st.text_input("Razón social *", kyc()["razon_social"])
        with c2:
            kyc()["nit_sin_dv"] = st.text_input("NIT sin dígito de verificación *", kyc()["nit_sin_dv"])

        c3, c4 = st.columns(2)
        with c3:
            idx_ent = ENTITY_TYPES.index(kyc()["tipo_entidad"]) if kyc()["tipo_entidad"] in ENTITY_TYPES else 1
            kyc()["tipo_entidad"] = st.selectbox("Tipo de entidad", ENTITY_TYPES, index=idx_ent)
        with c4:
            idx_sag = SI_NO.index(kyc()["obligado_sagrilaft"]) if kyc()["obligado_sagrilaft"] in SI_NO else 1
            kyc()["obligado_sagrilaft"] = st.selectbox(
                "¿Obligada a SAGRILAFT / SARLAFT / SIPLA / SIPLAFT?",
                SI_NO,
                index=idx_sag
            )

    # -------------------------
    # Información comercial
    # -------------------------
    with st.expander("Información comercial", expanded=False):
        kyc()["actividad_economica"] = st.text_area(
            "Descripción actividad económica",
            kyc()["actividad_economica"],
            height=80
        )
        c1, c2 = st.columns(2)
        with c1:
            kyc()["ciiu_principal"] = st.text_input("Código CIIU principal", kyc()["ciiu_principal"])
        with c2:
            kyc()["ciiu_otros"] = st.text_input("Código CIIU otros", kyc()["ciiu_otros"])

    # -------------------------
    # Información de contacto
    # -------------------------
    with st.expander("Información de contacto", expanded=False):
        kyc()["direccion_principal"] = st.text_input("Dirección principal", kyc()["direccion_principal"])

        c1, c2, c3 = st.columns(3)
        with c1:
            kyc()["ciudad"] = st.text_input("Ciudad", kyc()["ciudad"])
        with c2:
            kyc()["departamento"] = st.text_input("Departamento", kyc()["departamento"])
        with c3:
            kyc()["pais"] = st.text_input("País", kyc()["pais"])

        kyc()["pagina_web"] = st.text_input("Página web", kyc()["pagina_web"])

        c4, c5 = st.columns(2)
        with c4:
            kyc()["nombre_contacto_principal"] = st.text_input("Nombre contacto principal", kyc()["nombre_contacto_principal"])
        with c5:
            kyc()["cargo_contacto"] = st.text_input("Cargo", kyc()["cargo_contacto"])

        c6, c7, c8 = st.columns(3)
        with c6:
            kyc()["telefono_contacto"] = st.text_input("Teléfono", kyc()["telefono_contacto"])
        with c7:
            kyc()["celular_contacto"] = st.text_input("Celular", kyc()["celular_contacto"])
        with c8:
            kyc()["email_contacto"] = st.text_input("Email", kyc()["email_contacto"])

        c9, c10 = st.columns(2)
        with c9:
            kyc()["tel_area_contable"] = st.text_input("Teléfono área Contable", kyc()["tel_area_contable"])
        with c10:
            kyc()["tel_area_tesoreria"] = st.text_input("Teléfono área Tesorería", kyc()["tel_area_tesoreria"])

        kyc()["email_cert_tributarios"] = st.text_input("E-mail recepción certificados tributarios", kyc()["email_cert_tributarios"])
        kyc()["email_soportes_pago"] = st.text_input("E-mail recepción soportes de pago", kyc()["email_soportes_pago"])
        kyc()["email_fact_electronica"] = st.text_input("Email recepción facturación electrónica", kyc()["email_fact_electronica"])

    # -------------------------
    # Representante Legal
    # -------------------------
    with st.expander("Representante Legal", expanded=False):
        c1, c2, c3 = st.columns([3, 1, 2])
        with c1:
            kyc()["rep_nombre"] = st.text_input("Nombre y apellidos *", kyc()["rep_nombre"])
        with c2:
            idx_doc = DOC_TYPES.index(kyc()["rep_tipo_id"]) if kyc()["rep_tipo_id"] in DOC_TYPES else 0
            kyc()["rep_tipo_id"] = st.selectbox("Tipo de ID", DOC_TYPES, index=idx_doc)
        with c3:
            kyc()["rep_numero"] = st.text_input("Número", kyc()["rep_numero"])

        c4, c5, c6 = st.columns(3)
        with c4:
            kyc()["rep_telefono"] = st.text_input("Teléfono", kyc()["rep_telefono"])
        with c5:
            kyc()["rep_celular"] = st.text_input("Celular", kyc()["rep_celular"])
        with c6:
            kyc()["rep_email"] = st.text_input("Email", kyc()["rep_email"])

        st.markdown("**Preguntas de cumplimiento (PEP / reconocimiento / recursos públicos)**")
        q1, q2, q3, q4 = st.columns(4)
        with q1:
            kyc()["rep_pep"] = st.selectbox("¿Representante PEP?", SI_NO, index=SI_NO.index(kyc()["rep_pep"]) if kyc()["rep_pep"] in SI_NO else 1)
        with q2:
            kyc()["rep_reconocimiento"] = st.selectbox("¿Reconocimiento público?", SI_NO, index=SI_NO.index(kyc()["rep_reconocimiento"]) if kyc()["rep_reconocimiento"] in SI_NO else 1)
        with q3:
            kyc()["rep_recursos_publicos"] = st.selectbox("¿Maneja recursos públicos?", SI_NO, index=SI_NO.index(kyc()["rep_recursos_publicos"]) if kyc()["rep_recursos_publicos"] in SI_NO else 1)
        with q4:
            kyc()["rep_vinculo_pep"] = st.selectbox("¿Vínculo con PEP?", SI_NO, index=SI_NO.index(kyc()["rep_vinculo_pep"]) if kyc()["rep_vinculo_pep"] in SI_NO else 1)

        kyc()["rep_especificacion"] = st.text_area(
            "Si alguna respuesta es afirmativa, por favor especifique",
            kyc()["rep_especificacion"],
            height=80
        )

    # -------------------------
    # Composición Accionaria
    # -------------------------
    with st.expander("Composición Accionaria y Beneficiarios Finales", expanded=False):
        st.info("Agrega accionistas/socios (directa o indirectamente) con más del 5% de participación.")
        st.session_state.accionistas = st.data_editor(
            st.session_state.accionistas,
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "Tipo de ID": st.column_config.SelectboxColumn(options=DOC_TYPES),
                "¿PEP?": st.column_config.SelectboxColumn(options=SI_NO),
                "% Participación": st.column_config.NumberColumn(min_value=0, max_value=100, step=1),
            }
        )

    # -------------------------
    # Información Tributaria
    # -------------------------
    with st.expander("Información Tributaria", expanded=False):
        c1, c2 = st.columns(2)
        with c1:
            idx_reg = REGIMEN.index(kyc()["regimen"]) if kyc()["regimen"] in REGIMEN else 0
            kyc()["regimen"] = st.selectbox("Régimen al que pertenece la empresa", REGIMEN, index=idx_reg)
        with c2:
            kyc()["gran_contribuyente"] = st.selectbox("¿La empresa es gran contribuyente?", SI_NO, index=SI_NO.index(kyc()["gran_contribuyente"]) if kyc()["gran_contribuyente"] in SI_NO else 1)

        kyc()["num_resolucion_gc"] = st.text_input("Número de resolución (si aplica)", kyc()["num_resolucion_gc"])
        kyc()["calidad_iva"] = st.text_input("Calidad respecto al IVA", kyc()["calidad_iva"])

        c3, c4, c5, c6 = st.columns(4)
        with c3:
            kyc()["agente_retencion_fuente"] = st.selectbox("¿Agente retención en la fuente?", SI_NO,
                                                           index=SI_NO.index(kyc()["agente_retencion_fuente"]) if kyc()["agente_retencion_fuente"] in SI_NO else 1)
        with c4:
            kyc()["sujeta_retencion_fuente"] = st.selectbox("¿Sujeta a retención en la fuente?", SI_NO,
                                                           index=SI_NO.index(kyc()["sujeta_retencion_fuente"]) if kyc()["sujeta_retencion_fuente"] in SI_NO else 1)
        with c5:
            kyc()["autorretenedor_renta"] = st.selectbox("¿Autorretenedor en renta?", SI_NO,
                                                        index=SI_NO.index(kyc()["autorretenedor_renta"]) if kyc()["autorretenedor_renta"] in SI_NO else 1)
        with c6:
            kyc()["responsable_ica"] = st.selectbox("¿Responsable de ICA?", SI_NO,
                                                   index=SI_NO.index(kyc()["responsable_ica"]) if kyc()["responsable_ica"] in SI_NO else 1)

        kyc()["ciudades_ica"] = st.text_input("Ciudades ICA (si aplica)", kyc()["ciudades_ica"])

        c7, c8 = st.columns(2)
        with c7:
            kyc()["autorretenedor_ica"] = st.selectbox("¿Autorretenedor de ICA?", SI_NO,
                                                      index=SI_NO.index(kyc()["autorretenedor_ica"]) if kyc()["autorretenedor_ica"] in SI_NO else 1)
        with c8:
            kyc()["resolucion_ica_fecha"] = st.text_input("Número de resolución y fecha (ICA)", kyc()["resolucion_ica_fecha"])

    # -------------------------
    # Información Bancaria
    # -------------------------
    with st.expander("Información Bancaria", expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            kyc()["entidad_bancaria"] = st.text_input("Entidad bancaria", kyc()["entidad_bancaria"])
        with c2:
            kyc()["num_cuenta"] = st.text_input("Número de cuenta bancaria", kyc()["num_cuenta"])
        with c3:
            idx_tc = TIPO_CUENTA.index(kyc()["tipo_cuenta"]) if kyc()["tipo_cuenta"] in TIPO_CUENTA else 0
            kyc()["tipo_cuenta"] = st.selectbox("Tipo de cuenta", TIPO_CUENTA, index=idx_tc)

    # -------------------------
    # Información Financiera
    # -------------------------
    with st.expander("Información Financiera (Último año fiscal)", expanded=False):
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            kyc()["ing_operacionales"] = st.number_input("Ingresos operacionales ($)", min_value=0, value=int(kyc()["ing_operacionales"]), step=10)
        with c2:
            kyc()["ing_no_operacionales"] = st.number_input("Ingresos no operacionales ($)", min_value=0, value=int(kyc()["ing_no_operacionales"]), step=10)
        with c3:
            kyc()["egresos"] = st.number_input("Egresos ($)", min_value=0, value=int(kyc()["egresos"]), step=10)
        with c4:
            kyc()["activo_corriente"] = st.number_input("Activo corriente ($)", min_value=0, value=int(kyc()["activo_corriente"]), step=10)

        c5, c6, c7, c8 = st.columns(4)
        with c5:
            kyc()["total_activo"] = st.number_input("Total activo ($)", min_value=0, value=int(kyc()["total_activo"]), step=10)
        with c6:
            kyc()["pasivo_corriente"] = st.number_input("Pasivo corriente ($)", min_value=0, value=int(kyc()["pasivo_corriente"]), step=10)
        with c7:
            kyc()["total_pasivo"] = st.number_input("Total pasivo ($)", min_value=0, value=int(kyc()["total_pasivo"]), step=10)
        with c8:
            kyc()["patrimonio"] = st.number_input("Patrimonio ($)", min_value=0, value=int(kyc()["patrimonio"]), step=10)

        kyc()["detalle_ing_no_op"] = st.text_area("Detalle de ingresos no operacionales", kyc()["detalle_ing_no_op"], height=70)

    # -------------------------
    # Actividades en operaciones internacionales
    # -------------------------
    with st.expander("Actividades en operaciones internacionales", expanded=False):
        c1, c2 = st.columns(2)
        with c1:
            kyc()["trx_moneda_extranjera"] = st.selectbox("¿Realiza transacciones en moneda extranjera?", SI_NO,
                                                         index=SI_NO.index(kyc()["trx_moneda_extranjera"]) if kyc()["trx_moneda_extranjera"] in SI_NO else 1)
        with c2:
            kyc()["cual_moneda"] = st.text_input("¿Cuál(es)?", kyc()["cual_moneda"])

        c3, c4 = st.columns(2)
        with c3:
            kyc()["prod_fin_exterior"] = st.selectbox("¿Posee productos financieros en el exterior?", SI_NO,
                                                     index=SI_NO.index(kyc()["prod_fin_exterior"]) if kyc()["prod_fin_exterior"] in SI_NO else 1)
        with c4:
            kyc()["cuentas_moneda_extranjera"] = st.selectbox("¿Posee cuentas en moneda extranjera?", SI_NO,
                                                             index=SI_NO.index(kyc()["cuentas_moneda_extranjera"]) if kyc()["cuentas_moneda_extranjera"] in SI_NO else 1)

        kyc()["tipo_producto_exterior"] = st.text_input("Tipo de producto (si aplica)", kyc()["tipo_producto_exterior"])

    # -------------------------
    # Declaración + Autorización (SOLO 2 CHECKS, sin OTP)
    # -------------------------
    with st.expander("Declaración, Autorización y Términos y Condiciones", expanded=True):
        st.info(
            "Declaro que la actividad es lícita y que la información suministrada es veraz y verificable. "
            "Este texto está resumido en la demo (solo visual)."
        )

        kyc()["acepta_tratamiento_datos"] = st.checkbox(
            "Autorizo el tratamiento de datos personales.",
            value=kyc()["acepta_tratamiento_datos"]
        )
        kyc()["acepta_tyc"] = st.checkbox(
            "Acepto los Términos y Condiciones de Yamaha.",
            value=kyc()["acepta_tyc"]
        )

    # -------------------------
    # Botón CONTINUAR a la derecha (debajo de acordeones)
    # -------------------------
    st.session_state.p1_ready = bool(kyc()["acepta_tratamiento_datos"] and kyc()["acepta_tyc"])

    left, right = st.columns([3, 1])
    with left:
        if st.session_state.p1_ready:
            st.success("✅ Listo: puedes continuar al Paso 2 para cargar documentación.")
        else:
            st.warning("⚠️ Para habilitar Continuar, marca los 2 checks (Tratamiento de datos y T&C).")

    with right:
        st.markdown('<div class="btn-right">', unsafe_allow_html=True)
        if st.button("Continuar →", disabled=not st.session_state.p1_ready, use_container_width=True):
            st.session_state.step = 1
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    card_close()


# ==========================================================
# 8) PASO 2: Documentación (subir archivos)
# ==========================================================
def paso_2():
    card_open("Paso 2 | Documentación", "Carga o selecciona los anexos requeridos (solo visual, sin backend).")

    st.info("Esta sección simula la carga de documentos. No se almacena nada (demo front).")

    st.markdown("### Checklist de Anexos")
    anexos = [
        "Formulario de vinculación diligenciado y firmado por el representante legal",
        "RUT con fecha de expedición no mayor a 30 días",
        "Certificado de Cámara de comercio no mayor a 30 días",
        "Estados financieros del último cierre comparativo con notas (firmados)",
        "Certificado bancario relacionando número de cuenta",
        "Copia cédula representante legal",
        "Declaración de renta de los últimos dos años (clientes Wholesale)",
        "Certificado de composición accionaria",
        "Anexo PEPS (si aplica)",
    ]
    for a in anexos:
        st.checkbox(a, value=False)

    st.markdown("### Cargar archivos (DEMO)")

    files = st.file_uploader(
        "Subir documentos",
        accept_multiple_files=True,
        type=["pdf", "png", "jpg", "jpeg", "doc", "docx", "xls", "xlsx"]
    )
    st.session_state.last_upload_count = len(files) if files else 0

    # ✅ DEFINE nav_l y nav_r ANTES de usarlos
    nav_l, nav_r = st.columns([1, 1])

    with nav_l:
        if st.button("← Volver a Paso 1", use_container_width=True):
            st.session_state.step = 0
            st.rerun()

    with nav_r:
        uploaded = st.session_state.get("last_upload_count", 0) > 0
        if st.button("Enviar a estudio →", disabled=not uploaded, use_container_width=True):
            st.session_state.show_submit_modal = True
            st.rerun()


    # card_close()


# ==========================================================
# 9) RENDER según paso actual
# ==========================================================
# =========================
# ROUTER PRINCIPAL (por página)
# =========================
if st.session_state.page == "Solicitar crédito":
    # Dentro de Solicitar, usamos el step (Paso 1 / Paso 2)
    if st.session_state.step == 0:
        paso_1()
    elif st.session_state.step == 1:
        paso_2()
    else:
        render_placeholder(
            f"{STEP_MODELS[st.session_state.step]['title']} | {STEP_MODELS[st.session_state.step]['desc']}",
            "Sección demo pendiente. Por ahora están implementados Paso 1 y Paso 2."
        )

elif st.session_state.page == "Estudio crédito":
    render_estudio_credito()

elif st.session_state.page == "Formalización":
    render_formalizacion()

elif st.session_state.page == "Pendientes":
    render_pendientes_congelado()


elif st.session_state.page == "Finalización":
    render_finalizacion()



else:
    render_placeholder("Finalización", "Parte final demo pendiente.")

# El modal siempre al final para que quede por encima
if st.session_state.show_submit_modal:
    submit_dialog()