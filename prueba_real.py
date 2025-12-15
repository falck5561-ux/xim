import google.generativeai as genai

# Tu clave actual
API_KEY = "AIzaSyAFKkY4AUfkbpT1QAdKNrxfTeTGhsjmdR4"
genai.configure(api_key=API_KEY)

print("--- DIAGNÓSTICO DE POCHITA ---")
try:
    print(f"Probando clave que termina en: ...{API_KEY[-4:]}")
    
    # Listar modelos
    mis_modelos = []
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            mis_modelos.append(m.name)
            print(f"✅ MODELO DISPONIBLE: {m.name}")

    if not mis_modelos:
        print("\n❌ ALERTA ROJA: La clave es válida, pero la lista de modelos está VACÍA.")
        print("Posibles causas:")
        print("1. La API 'Google AI Studio' no se activó correctamente al crear la clave.")
        print("2. Restricción regional (aunque en México debería funcionar).")
    else:
        print(f"\n✨ ¡Éxito! Tienes acceso a {len(mis_modelos)} modelos.")
        print(f"Sugerencia: Usa el nombre '{mis_modelos[0]}' en tu views.py")

except Exception as e:
    print(f"\n💀 ERROR FATAL DE CONEXIÓN: {e}")