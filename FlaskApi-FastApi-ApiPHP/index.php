<?php

// Configuración de la base de datos SQLite
$DB_FILE = __DIR__ . '/db.sqlite';
$db = new SQLite3($DB_FILE);
$db->exec('CREATE TABLE IF NOT EXISTS datos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    direccion TEXT,
    telefono TEXT,
    email TEXT
)');

// Función para obtener todos los datos
function obtenerDatos($db) {
    $datos = [];
    $result = $db->query('SELECT * FROM datos');
    while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
        $datos[] = $row;
    }
    return $datos;
}

// Función para eliminar un dato por ID
function eliminarDato($db, $datoId) {
    $stmt = $db->prepare('DELETE FROM datos WHERE id = :id');
    $stmt->bindValue(':id', $datoId, SQLITE3_INTEGER);
    $result = $stmt->execute();
    if (!$result) {
        return ['status' => 500, 'message' => 'Error en el servidor'];
    } elseif ($db->changes() === 0) {
        return ['status' => 404, 'message' => 'Dato no encontrado'];
    } else {
        return ['status' => 200, 'message' => 'Dato eliminado correctamente'];
    }
}

// Función para agregar un nuevo dato
function agregarDato($db, $data) {
    $nombre = $data['nombre'] ?? '';
    $direccion = $data['direccion'] ?? '';
    $telefono = $data['telefono'] ?? '';
    $email = $data['email'] ?? '';
    $stmt = $db->prepare('INSERT INTO datos (nombre, direccion, telefono, email) VALUES (:nombre, :direccion, :telefono, :email)');
    $stmt->bindValue(':nombre', $nombre, SQLITE3_TEXT);
    $stmt->bindValue(':direccion', $direccion, SQLITE3_TEXT);
    $stmt->bindValue(':telefono', $telefono, SQLITE3_TEXT);
    $stmt->bindValue(':email', $email, SQLITE3_TEXT);
    $result = $stmt->execute();
    if (!$result) {
        return ['status' => 500, 'message' => 'Error en el servidor'];
    } else {
        return ['status' => 201, 'message' => 'Dato agregado correctamente'];
    }
}

// Ruta para manejar solicitudes
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    $datos = obtenerDatos($db);
    header('Content-Type: application/json');
    echo json_encode(['datos' => $datos]);
} elseif ($_SERVER['REQUEST_METHOD'] === 'DELETE') {
    $datoId = $_GET['id'] ?? null;
    if ($datoId === null) {
        http_response_code(400);
        echo json_encode(['message' => 'ID de dato no proporcionado']);
    } else {
        $resultado = eliminarDato($db, $datoId);
        http_response_code($resultado['status']);
        echo json_encode(['message' => $resultado['message']]);
    }
} elseif ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $input = json_decode(file_get_contents('php://input'), true);
    $resultado = agregarDato($db, $input);
    http_response_code($resultado['status']);
    echo json_encode(['message' => $resultado['message']]);
}
