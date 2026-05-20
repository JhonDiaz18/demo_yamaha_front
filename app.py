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
    "📊 Estudio crédito",
    "Resultado / Seguimiento",
]

# Stepper horizontal (con lanchas). Paso 1 y Paso 2 reales, resto demo.
STEP_MODELS = [
    {"key": "p1", "title": "Paso 1", "desc": "Conocimiento del cliente", "icon": "boatSvg"},
    {"key": "p2", "title": "Paso 2", "desc": "Documentación", "icon": "boatSvg2"},
    {"key": "p3", "title": "Paso 3", "desc": "Validaciones (demo)", "icon": "boatSvg"},
    {"key": "p4", "title": "Paso 4", "desc": "Análisis (demo)", "icon": "boatSvg2"},
    {"key": "p5", "title": "Paso 5", "desc": "Producto (demo)", "icon": "boatSvg"},
    {"key": "p6", "title": "Paso 6", "desc": "Respuesta (demo)", "icon": "boatSvg2"},
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

    



init_state()


# ==========================================================
# 3) UI: SIDEBAR + HERO
# ==========================================================
with st.sidebar:
    st.markdown("### Panel de administración")
    st.session_state.page = st.radio(
        "Menú",
        MENU,
        index=MENU.index(st.session_state.page) if st.session_state.page in MENU else 0,
        label_visibility="collapsed"
    )
    st.divider()
    st.caption("Demo solo visual (Front). Modo claro.")


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


render_stepper(st.session_state.step)


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

def render_submit_modal():
    """Modal que aparece al finalizar Paso 2."""
    if not st.session_state.show_submit_modal:
        return

    st.markdown(
        """
        <div class="modal-overlay">
          <div class="modal">
            <div class="modal-title">✅ Solicitud radicada</div>
            <div class="modal-text">
              Tu solicitud pasará a <b>Estudio de crédito</b>. <br/>
              En la demo podrás ver cómo se evaluaría el caso con ejemplos ficticios.
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Acciones con botones (debajo del HTML, para que Streamlit capture eventos)
    a1, a2 = st.columns([3, 1])
    with a1:
        if st.button("Ir a Estudio de crédito", key="modal_go_study", use_container_width=True):
            st.session_state.show_submit_modal = False
            st.session_state.page = "📊 Estudio crédito"
            st.rerun()
    with a2:
        if st.button("Cerrar", key="modal_close", use_container_width=True):
            st.session_state.show_submit_modal = False
            st.rerun()

# ==========================================================
# 6) RUTEO (en Parte 2 implementamos contenido real de Paso 1 y Paso 2)
# ==========================================================
def render_placeholder(title: str, msg: str):
    card_open(title, "")
    st.info(msg)
    card_close()

# --- FIN PARTE 1/2 ---
# En la PARTE 2/2 vamos a:
# - Construir Paso 1 con acordeones (sin fecha, producto Wholesale, modalidad Marina)
# - Al final: checks T&C (2 checks) y botón "Continuar" a la derecha para ir al Paso 2
# - Paso 2: subir documentación (uploader + checklist)

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
        c1, c2, c3 = st.columns([1.2, 1.2, 1.2])
        with c1:
            kyc()["tipo_solicitud"] = st.selectbox(
                "Tipo de Solicitud",
                ["Creación", "Actualización"],
                index=["Creación", "Actualización"].index(kyc()["tipo_solicitud"])
            )
        with c2:
            # Producto predeterminado Wholesale
            default_prod = PRODUCTOS.index(kyc()["producto"]) if kyc()["producto"] in PRODUCTOS else 0
            kyc()["producto"] = st.selectbox("Producto", PRODUCTOS, index=default_prod)
        with c3:
            # Modalidad predeterminada Marina
            default_mod = MODALIDADES.index(kyc()["modalidad"]) if kyc()["modalidad"] in MODALIDADES else 0
            kyc()["modalidad"] = st.selectbox("Modalidad", MODALIDADES, index=default_mod)

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
if st.session_state.step == 0:
    paso_1()
elif st.session_state.step == 1:
    paso_2()
else:
    render_placeholder(
        f"{STEP_MODELS[st.session_state.step]['title']} | {STEP_MODELS[st.session_state.step]['desc']}",
        "Sección demo pendiente. Por ahora están implementados Paso 1 y Paso 2."
    )

render_submit_modal()