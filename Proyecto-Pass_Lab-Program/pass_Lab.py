import hashlib
import time
import random
import string
import matplotlib.pyplot as plt
import csv

# Función para generar hash SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# 1. Generar 100 contraseñas de prueba (con validacion de hashes unicos)
def generate_test_passwords(filename="contraseñas.txt", hashed_filename="contraseñas_hash.txt"):
    passwords = []
    hash_set = set()
    for i in range(50):
        length = random.randint(4, 7)
        password = ''.join(random.choices(string.ascii_lowercase, k=length))
        if i < 5:  # Forzar 5 contraseñas debiles que coincidan con el diccionario
            password = ["password", "123456", "qwerty", "abc123", "letmein"][i]
        pwd_hash = hash_password(password)
        while pwd_hash in hash_set:
            password = ''.join(random.choices(string.ascii_lowercase, k=length))
            pwd_hash = hash_password(password)
        hash_set.add(pwd_hash)
        passwords.append(f"user{i+1}:{password}")
    for i in range(50, 100):
        length = random.randint(8, 12)
        password = ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%", k=length))
        pwd_hash = hash_password(password)
        while pwd_hash in hash_set:
            password = ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%", k=length))
            pwd_hash = hash_password(password)
        hash_set.add(pwd_hash)
        passwords.append(f"user{i+1}:{password}")
    
    with open(filename, 'w') as f:
        for entry in passwords:
            f.write(entry + '\n')
    
    with open(hashed_filename, 'w') as f:
        for entry in passwords:
            user, pwd = entry.split(':')
            hashed_pwd = hash_password(pwd)
            f.write(f"{user}:{hashed_pwd}\n")
    
    return passwords

# 2. Generar diccionario de prueba
def generate_dictionary(filename="diccionario.txt"):
    palabras_comunes = [
        "password", "123456", "qwerty", "abc123", "letmein",
        "admin", "test", "pass", "1234", "hello",
        "welcome", "login", "secret", "password1", "user"
    ] * 10
    with open(filename, 'w') as f:
        for palabra in palabras_comunes:
            f.write(palabra + '\n')

# 3. Ataque de diccionario
def dictionary_attack(hashed_filename="contraseñas_hash.txt", dict_filename="diccionario.txt"):
    start_time = time.time()
    contraseñas_recuperadas = []
    
    with open(hashed_filename, 'r') as f:
        contraseñas_hash = {line.split(':')[0]: line.strip().split(':')[1] for line in f}
    
    with open(dict_filename, 'r') as f:
        for palabra in f:
            palabra = palabra.strip()
            hash_palabra = hash_password(palabra)
            for usuario, hash_contraseña in list(contraseñas_hash.items()):
                if hash_palabra == hash_contraseña:
                    contraseñas_recuperadas.append((usuario, palabra))
                    del contraseñas_hash[usuario]
    
    end_time = time.time()
    tiempo_ejecucion = end_time - start_time
    return contraseñas_recuperadas, tiempo_ejecucion

# 4. Generar visualizaciones con Matplotlib
def generate_visualizations(contraseñas_recuperadas, total_contraseñas=100):
    # Gráfico de barras: contraseñas recuperadas vs. no recuperadas
    cantidad_recuperadas = len(contraseñas_recuperadas)
    cantidad_no_recuperadas = total_contraseñas - cantidad_recuperadas
    plt.figure(figsize=(8, 6))
    plt.bar(['Recuperadas', 'No recuperadas'], [cantidad_recuperadas, cantidad_no_recuperadas], color=['#1f77b4', '#ff7f0e'])
    plt.title('Contraseaas Recuperadas vs. No Recuperadas', fontsize=14)
    plt.ylabel('Cantidad', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig('cracked_passwords_bar.png')
    plt.close()
    
    # Gráfico circular: contraseñas recuperadas débiles vs. fuertes (solo si hay contraseñas recuperadas)
    if contraseñas_recuperadas:  # Verifica que la lista no esté vacía
        cantidad_debiles = sum(1 for _, pwd in contraseñas_recuperadas if len(pwd) < 8)
        cantidad_fuertes = len(contraseñas_recuperadas) - cantidad_debiles
        etiquetas = ['Debiles (< 8 caracteres)', 'Fuertes (≥ 8 caracteres)']
        medidas = [cantidad_debiles, cantidad_fuertes]
        colores = ['#ff9999', '#66b3ff']
        plt.figure(figsize=(8, 6))
        plt.pie(medidas, labels=etiquetas, colors=colores, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 12})
        plt.title('Distribucion de contraseñas recuperadas por Longitud', fontsize=14)
        plt.savefig('password_length_pie.png')
        plt.close()
    else:
        print("No se recuperaron contrasenas, se omite el grafico circular.")

    # Histograma adicional: distribucion de longitudes de contraseñas recuperadas (solo si hay contraseñas)
    if contraseñas_recuperadas:
        longitudes = [len(pwd) for _, pwd in contraseñas_recuperadas]
        plt.figure(figsize=(8, 6))
        plt.hist(longitudes, bins=range(4, 13), color='#2ca02c', edgecolor='black')
        plt.title('Histograma de longitudes de contrasenas recuperadas', fontsize=14)
        plt.xlabel('Longitud de contraseña', fontsize=12)
        plt.ylabel('Frecuencia', fontsize=12)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.savefig('password_length_histogram.png')
        plt.close()
    else:
        print("No se recuperaron contrasenas, se omite el histograma.")

# 5. Generar recomendaciones y resultados
def generate_recommendations(contraseñas_recuperadas, tiempo_ejecucion, output_filename="resultados.txt", csv_filename="cracked_passwords.csv"):
    recomendaciones = []
    for usuario, contraseña in contraseñas_recuperadas:
        rec = f"Usuario: {usuario}, Contrasena: {contraseña}\n"
        if len(contraseña) < 8:
            rec += " Recomendacion: La contrasena tiene menos de 8 caracteres. Usar al menos 8 caracteres.\n"
        rec += " Recomendacion general: Incluir letras mayusculas, minusculas, numeros y caracteres especiales.\n"
        recomendaciones.append(rec)
    
    with open(output_filename, 'w') as f:
        f.write(f"Contrasenas recuperadas: {len(contraseñas_recuperadas)}\n")
        f.write(f"Tiempo de ejecucion: {tiempo_ejecucion:.2f} segundos\n\n")
        f.write("Descripcion de visualizaciones:\n")
        f.write(" cracked_passwords_bar.png: Grafico de barras que muestra contrasenas recuperadas vs. no recuperadas.\n")
        f.write(" password_length_pie.png: Grafico circular que clasifica contrasenas recuperadas por longitud.\n")
        f.write(" password_length_histogram.png: Histograma de distribucion de longitudes de contrasenas recuperadas.\n\n")
        f.write("Recomendaciones:\n")
        for rec in recomendaciones:
            f.write(rec + '\n')
    
    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Usuario', 'Contrasena Recuperada', 'Longitud', 'Recomendacion'])
        for usuario, contraseña in contraseñas_recuperadas:
            rec = "Usar >=8 chars" if len(contraseña) < 8 else "Fuerte, pero mejorar complejidad"
            writer.writerow([usuario, contraseña, len(contraseña), rec])
    
    return recomendaciones

# Ejecución principal
if __name__ == "__main__":
    print("Generando contraseñas de prueba...")
    passwords = generate_test_passwords()
    print("Generando diccionario de prueba...")
    generate_dictionary()
    print("Ejecutando ataque de diccionario...")
    contraseñas_recuperadas, tiempo_ejecucion = dictionary_attack()
    print("Generando visualizaciones...")
    generate_visualizations(contraseñas_recuperadas)
    print("Generando recomendaciones...")
    recomendaciones = generate_recommendations(contraseñas_recuperadas, tiempo_ejecucion)
    saved_graphs = ["cracked_passwords_bar.png"]
    if contraseñas_recuperadas:
        saved_graphs.extend(["password_length_pie.png", "password_length_histogram.png"])
    print(f"Completado. Resultados guardados en resultados.txt y cracked_passwords.csv")
    print(f"Graficos guardados: {', '.join(saved_graphs)}")
    print(f"Contrasenas recuperadas: {len(contraseñas_recuperadas)}")
    print(f"Tiempo de ejecucion: {tiempo_ejecucion:.2f} segundos")