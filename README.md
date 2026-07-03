# proyectodeflor
Vaneesa nunca me hará caso, :( al final le acepto la solcitud de seguimiento a vivian y la stlakeamo jajajjajajajjjaajjaja :(

Importar el script:

```bash
mysql -u root -p < script_sistema_reservas.sql
```

### Cambios

| Cambio | Por qué |
|--------|---------|
| `Email ... UNIQUE` | Evita usuarios duplicados con el mismo correo. En un sistema de login el email es identificador único. |
| `EstadoReserva ENUM('Confirmada','Pendiente','Cancelada')` | Restringe el estado a valores válidos. Antes era `VARCHAR` libre y aceptaba cualquier texto. |
| `NOT NULL` en campos clave | Impide filas incompletas (una reserva sin fecha o sin usuario no tiene sentido). |
| `DEFAULT TRUE` / `DEFAULT 'Pendiente'` | Valores razonables por defecto: una habitación nueva está disponible, una reserva nueva queda pendiente. |
| `Economica` sin acento | Evita caracteres corruptos al importar si la conexión no está en UTF-8. |



## Correr la API

```bash
python app.py
```

Queda en `http://localhost:5000`  o el que vayas a usar.

## Endpoints

| Recurso | Métodos |
|---------|---------|
| `/usuarios` | GET, POST |
| `/usuarios/<id>` | GET, PUT, DELETE |
| `/habitaciones` | GET, POST |
| `/habitaciones/<id>` | GET, PUT |
| `/reservaciones` | GET, POST |
| `/reservaciones/<id>` | GET, PUT |

Códigos: `200` ok, `201` creado, `400` datos inválidos, `404` no encontrado, `500` error de BD.

## Probar con Postman

1. **Import** → seleccionar `SistemaReservas.postman_collection.json`.
2. Verificar la variable `base_url` (colección → Variables). Default: `http://localhost:5000`.
3. Levantar la API (`python app.py`) antes de mandar peticiones.
4. Abrir un request y presionar **Send**. Los POST/PUT ya traen el body de ejemplo en **Body → raw**.

### Orden para evidencias

```
GET  /usuarios          -> lista los 5 iniciales
POST /usuarios          -> crea uno nuevo (201)
GET  /usuarios          -> aparece el nuevo
POST /reservaciones     -> crea una reserva
PUT  /reservaciones/1   -> actualiza el estado
```
