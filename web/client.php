<?php

$payload = ['server_name' => $_GET['server_name'], 'player_name' => $_GET['player_name'], 'secret_key' => $_GET['secret_key'], 'command' => $_GET['command']];

$socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
socket_connect($socket,'127.0.0.1', 1234);
$package = json_encode($payload);
socket_send($socket, $package, strlen($package), 0);

socket_close($socket);
