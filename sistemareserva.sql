CREATE DATABASE IF NOT EXISTS SistemaReservas;
USE SistemaReservas;

CREATE TABLE IF NOT EXISTS Usuarios (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(50) NOT NULL,
    Apellido VARCHAR(50) NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE,
    Contrasena VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS Habitaciones (
    RoomID INT AUTO_INCREMENT PRIMARY KEY,
    TipoHabitacion VARCHAR(50) NOT NULL,
    Descripcion TEXT,
    Precio DECIMAL(10,2) NOT NULL,
    Disponibilidad BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS Reservaciones (
    ReservationID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    RoomID INT NOT NULL,
    FechaInicio DATE NOT NULL,
    FechaFin DATE NOT NULL,
    EstadoReserva ENUM('Confirmada', 'Pendiente', 'Cancelada') NOT NULL DEFAULT 'Pendiente',
    FOREIGN KEY (UserID) REFERENCES Usuarios(UserID),
    FOREIGN KEY (RoomID) REFERENCES Habitaciones(RoomID)
);

INSERT INTO Usuarios (Nombre, Apellido, Email, Contrasena) VALUES
('Ana', 'Perez', 'ana@email.com', '123'),
('Luis', 'Gomez', 'luis@email.com', '123'),
('Maria', 'Lopez', 'maria@email.com', '123'),
('Juan', 'Ruiz', 'juan@email.com', '123'),
('Pedro', 'Diaz', 'pedro@email.com', '123');

INSERT INTO Habitaciones (TipoHabitacion, Descripcion, Precio, Disponibilidad) VALUES
('Individual', 'Cama sencilla', 500, TRUE),
('Doble', 'Dos camas', 800, TRUE),
('Suite', 'Vista al mar', 1500, TRUE),
('Matrimonial', 'Cama grande', 900, TRUE),
('Economica', 'Sin ventana', 300, TRUE);

INSERT INTO Reservaciones (UserID, RoomID, FechaInicio, FechaFin, EstadoReserva) VALUES
(1, 1, '2026-07-01', '2026-07-05', 'Confirmada'),
(2, 2, '2026-07-02', '2026-07-06', 'Pendiente'),
(3, 3, '2026-07-03', '2026-07-07', 'Confirmada'),
(4, 4, '2026-07-04', '2026-07-08', 'Cancelada'),
(5, 5, '2026-07-05', '2026-07-09', 'Confirmada');