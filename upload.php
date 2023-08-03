
<?php
if(isset($_FILES["file"]) and isset($_POST["format"])) {
    $file_name = $_FILES["file"]["name"];
    $file_tmp = $_FILES["file"]["tmp_name"];
    $file_type = $_FILES["file"]["type"];
    $file_size = $_FILES["file"]["size"];
    $new_file_format = $_POST["format"];

    $target_dir = "DataStorage/";
    if(!file_exists($target_dir)) mkdir($target_dir);
    $target_file = $target_dir.basename($file_name);

    if(move_uploaded_file($file_tmp, $target_file)) {
        echo "Файл успешно загружен.";
    } else {
        echo "Ошибка загрузки файла.";
    }
}
