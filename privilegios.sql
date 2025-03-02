CREATE USER 'usuario_snake'@'%' IDENTIFIED BY 'contraseña_segura';
GRANT ALL PRIVILEGES ON snake_voting.* TO 'usuario_snake'@'%';

SHOW GRANTS FOR 'usuario_snake'@'%';
