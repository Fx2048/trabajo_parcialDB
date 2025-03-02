Se siguió el siguiente procedimiento: 
![image](https://github.com/user-attachments/assets/3ca8e8a2-5f4e-4be1-a360-1ae4d5d7c6d1)

Portada del juego(Ventana 1)
![image](https://github.com/user-attachments/assets/5fd33e85-a015-4276-a0eb-03dd710d4da1)

Ventana de controles (Ventana 2)
![image](https://github.com/user-attachments/assets/8ddd2444-8f43-45b0-b442-5ca452fe95bd)

Ventana 3: Game OVer
![image](https://github.com/user-attachments/assets/b39e7401-1a77-4303-893b-976d12e594cc)

Capturas desde SQL: 

Diagrama

![image](https://github.com/user-attachments/assets/4a41bc0f-775d-4cb6-a837-2a807bccabe4)


Votaciones en directo:
![image](https://github.com/user-attachments/assets/b36be6e4-6dca-44ec-9bbc-15e4cc47d9f5)



### 🔹 **Cómo funciona la votación**
1. **Cada usuario tiene una ventana de votación (Tkinter)** donde puede elegir una dirección:  
   - Arriba (`"UP"`)  
   - Abajo (`"DOWN"`)  
   - Izquierda (`"LEFT"`)  
   - Derecha (`"RIGHT"`)  

2. **Cuando el usuario presiona un botón, se registra su voto en la base de datos MySQL.**  
   ```python
   def insertar_voto(direccion):
       conn = mysql.connector.connect(**DB_CONFIG)
       cursor = conn.cursor()
       cursor.execute("INSERT INTO votos (direccion) VALUES (%s)", (direccion,))
       conn.commit()
       conn.close()
   ```
   
3. **Cada `VOTE_INTERVAL` (3 segundos), el juego revisa los votos y decide la dirección mayoritaria.**  
   ```python
   def contar_votos():
       conn = mysql.connector.connect(**DB_CONFIG)
       cursor = conn.cursor()
       cursor.execute("SELECT direccion, COUNT(*) FROM votos WHERE procesado = 0 GROUP BY direccion")
       votos = cursor.fetchall()
       conn.close()
       
       if not votos:
           return None
       
       max_votos = max(votos, key=lambda x: x[1])
       return max_votos[0]
   ```

4. **El juego mueve la serpiente en la dirección ganadora** y marca los votos como procesados.  
   ```python
   def marcar_votos_como_procesados():
       conn = mysql.connector.connect(**DB_CONFIG)
       cursor = conn.cursor()
       cursor.execute("UPDATE votos SET procesado = 1")
       conn.commit()
       conn.close()
   ```

---

### 🔹 **Cómo se sincronizan las ventanas**
- **Todas las ventanas de votación se conectan a la misma base de datos MySQL** y registran votos en la tabla `votos`.  
- **El juego consulta la base de datos cada 3 segundos** para obtener la dirección más votada.  
- **Todos los usuarios pueden votar simultáneamente** y su voto es contado en tiempo real.  
- **El juego siempre usa los votos más recientes**, eliminando los procesados para evitar acumulaciones.

---

### 🔹 **Cómo se maneja el empate**
- **Si hay varias direcciones con la misma cantidad de votos, se elige una al azar.**  
  ```python
  def contar_votos():
      conn = mysql.connector.connect(**DB_CONFIG)
      cursor = conn.cursor()
      cursor.execute("SELECT direccion, COUNT(*) FROM votos WHERE procesado = 0 GROUP BY direccion")
      votos = cursor.fetchall()
      conn.close()
      
      if not votos:
          return None
      
      max_votos = max(votos, key=lambda x: x[1])[1]
      opciones_ganadoras = [voto[0] for voto in votos if voto[1] == max_votos]
      return random.choice(opciones_ganadoras)  # Se elige aleatoriamente en caso de empate
  ```
---

### 🔹 **Mejoras del sistema**
✅ **Votación en tiempo real**: Se pueden conectar múltiples jugadores y participar sin retrasos.  
✅ **Evita trampas**: No se permite votar dos veces en el mismo intervalo.  
✅ **Sincronización automática**: No depende de eventos manuales, sino de consultas periódicas.  
✅ **Escalabilidad**: Se puede alojar en un servidor MySQL remoto y permitir muchas conexiones simultáneas.  
✅ **Experiencia interactiva**: Permite a varios jugadores controlar un solo juego de manera democrática.

---


Esquema: 
Aquí tienes el esquema de la base de datos en SQL:

```sql
CREATE DATABASE IF NOT EXISTS snake_voting;
USE snake_voting;

CREATE TABLE IF NOT EXISTS votos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    direccion VARCHAR(10) NOT NULL,
    procesado TINYINT DEFAULT 0
);
```

### Explicación:
- **`CREATE DATABASE IF NOT EXISTS snake_voting;`** → Crea la base de datos si no existe.
- **`USE snake_voting;`** → Selecciona la base de datos para usarla.
- **`CREATE TABLE IF NOT EXISTS votos`** → Crea la tabla `votos` si no existe.
- **`id INT AUTO_INCREMENT PRIMARY KEY`** → Identificador único para cada voto.
- **`direccion VARCHAR(10) NOT NULL`** → Almacena la dirección del voto (`UP`, `DOWN`, `LEFT`, `RIGHT`).
- **`procesado TINYINT DEFAULT 0`** → Indica si el voto ha sido procesado (0 = No, 1 = Sí).


