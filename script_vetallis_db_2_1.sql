-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema vetallis_db_2_1
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema vetallis_db_2_1
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `vetallis_db_2_1` DEFAULT CHARACTER SET utf8 ;
SHOW WARNINGS;
USE `vetallis_db_2_1` ;

-- -----------------------------------------------------
-- Table `usuario`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `usuario` (
  `usuario_id` INT NOT NULL AUTO_INCREMENT,
  `usuario_senha` VARCHAR(15) NOT NULL,
  `usuario_email` VARCHAR(255) NOT NULL,
  `usuario_nome` VARCHAR(100) NOT NULL,
  `usuario_cpf` VARCHAR(11) NOT NULL,
  `usuario_cargo` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`usuario_id`)
)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `produto`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `produto` (
  `produto_id` INT NOT NULL AUTO_INCREMENT,
  `produto_nome` VARCHAR(100) NOT NULL,
  `produto_descricao` VARCHAR(100) NOT NULL,
  `produto_categoria` VARCHAR(20) NOT NULL,
  `usuario_usuario_id` INT NOT NULL,
  PRIMARY KEY (`produto_id`, `usuario_usuario_id`),
  CONSTRAINT `fk_produto_usuario1`
    FOREIGN KEY (`usuario_usuario_id`)
    REFERENCES `usuario` (`usuario_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)

ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `estoque`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `estoque` (
  `estoque_id` INT NOT NULL AUTO_INCREMENT,
  `estoque_quantidade` VARCHAR(45) NOT NULL,
  `estoque_observacao` VARCHAR(45) NULL,
  `produto_produto_id` INT NOT NULL,
  `produto_usuario_usuario_id` INT NOT NULL,
  PRIMARY KEY (`estoque_id`),
  CONSTRAINT `fk_estoque_produto1`
    FOREIGN KEY (`produto_produto_id` , `produto_usuario_usuario_id`)
    REFERENCES `produto` (`produto_id` , `usuario_usuario_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)

ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `lista_compra`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `lista_compra` (
  `lista_compra_id` INT NOT NULL AUTO_INCREMENT,
  `lista_compra_nome` VARCHAR(100) NOT NULL,
  `lista_compra_quantidade` INT NOT NULL,
  `lista_compra_valor` FLOAT NOT NULL,
  `lista_compra_status` VARCHAR(45) NOT NULL,
  `estoque_estoque_id` INT NOT NULL,
  PRIMARY KEY (`lista_compra_id`),
  CONSTRAINT `fk_lista_compra_estoque1`
    FOREIGN KEY (`estoque_estoque_id`)
    REFERENCES `estoque` (`estoque_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `sensor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sensor` (
  `sensor_id` INT NOT NULL AUTO_INCREMENT,
  `sensor_nome` VARCHAR(50) NOT NULL,
  `sensor_descricao` VARCHAR(150) NOT NULL,
  `sensor_n_serie` VARCHAR(50) NOT NULL,
  `sensor_modelo` VARCHAR(50) NOT NULL,
  `sensor_voltagem` VARCHAR(30) NOT NULL,
  `sensor_tipo_conexao` VARCHAR(50) NOT NULL,
  `sensor_localizacao` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`sensor_id`)
)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `dados_sensor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dados_sensor` (
  `dados_sensor_id` INT NOT NULL AUTO_INCREMENT,
  `dados_sensor_nome` VARCHAR(100) NOT NULL,
  `dados_sensor_tipo` VARCHAR(20) NOT NULL,
  `dados_sensor_local` VARCHAR(20) NOT NULL,
  `dados_sensor_status` VARCHAR(20) NOT NULL,
  `dados_sensor_data_install` DATE NOT NULL,
  `sensor_sensor_id` INT NOT NULL,
  PRIMARY KEY (`dados_sensor_id`),
  CONSTRAINT `fk_dados_sensor_sensor1`
    FOREIGN KEY (`sensor_sensor_id`)
    REFERENCES `sensor` (`sensor_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `fornecedor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `fornecedor` (
  `fornecedor_id` INT NOT NULL AUTO_INCREMENT,
  `fornecedor_nome` VARCHAR(100) NOT NULL,
  `fornecedor_cnpj` VARCHAR(14) NOT NULL,
  `fornecedor_endereço` VARCHAR(100) NOT NULL,
  `fornecedor_pedido_minimo` FLOAT NOT NULL,
  `fornecedor_tipo_produtos` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`fornecedor_id`)
)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `pedido_entrada`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pedido_entrada` (
  `pedido_entrada_id` INT NOT NULL AUTO_INCREMENT,
  `pedido_entrada_nome` VARCHAR(100) NOT NULL,
  `pedido_entrada_data` VARCHAR(10) NOT NULL,
  `pedido_entrada_status` VARCHAR(45) NOT NULL,
  `fornecedor_fornecedor_id` INT NOT NULL,
  PRIMARY KEY (`pedido_entrada_id`),
  CONSTRAINT `fk_pedido_entrada_fornecedor1`
    FOREIGN KEY (`fornecedor_fornecedor_id`)
    REFERENCES `fornecedor` (`fornecedor_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `item_pedido_entrada`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `item_pedido_entrada` (
  `item_pedido_entrada_id` INT NOT NULL AUTO_INCREMENT,
  `item_pedido_entrada_lote` VARCHAR(100) NOT NULL,
  `item_pedido_entrada_quantidade` INT NOT NULL,
  `item_pedido_entrada_data_validade` VARCHAR(10) NOT NULL,
  `item_pedido_entrada_valor_unitario` FLOAT NOT NULL,
  `pedido_entrada_pedido_entrada_id` INT NOT NULL,
  `item_pedido_entrada_nome` VARCHAR(45) NOT NULL,
  `estoque_estoque_id` INT NOT NULL,
  PRIMARY KEY (`item_pedido_entrada_id`),
  CONSTRAINT `fk_entrada_item_pedido_entrada1`
    FOREIGN KEY (`pedido_entrada_pedido_entrada_id`)
    REFERENCES `pedido_entrada` (`pedido_entrada_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_item_pedido_entrada_estoque1`
    FOREIGN KEY (`estoque_estoque_id`)
    REFERENCES `estoque` (`estoque_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `animal`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `animal` (
  `animal_id` INT NOT NULL AUTO_INCREMENT,
  `animal_espécie` VARCHAR(45) NOT NULL,
  `animal_quantidade` INT NOT NULL,
  `animal_sexo` VARCHAR(45) NOT NULL,
  `animal_raça` VARCHAR(45) NOT NULL,
  `animal_identificacao` VARCHAR(45) NOT NULL,
  `animal_idade` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`animal_id`)
)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `pedido_saida`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pedido_saida` (
  `pedido_saida_id` INT NOT NULL AUTO_INCREMENT,
  `pedido_saida_nome` VARCHAR(100) NOT NULL,
  `pedido_saida_data` VARCHAR(10) NOT NULL,
  `pedido_entrada_status` VARCHAR(45) NOT NULL,
  `animal_animal_id` INT NOT NULL,
  PRIMARY KEY (`pedido_saida_id`),
  CONSTRAINT `fk_pedido_saida_animal1`
    FOREIGN KEY (`animal_animal_id`)
    REFERENCES `animal` (`animal_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `item_pedido_saida`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `item_pedido_saida` (
  `item_pedido_saida_id` INT NOT NULL AUTO_INCREMENT,
  `item_pedido_saida_lote` VARCHAR(100) NOT NULL,
  `item_pedido_saida_quantidade` INT NOT NULL,
  `item_pedido_saida_data_validade` VARCHAR(10) NOT NULL,
  `pedido_saida_pedido_saida_id` INT NOT NULL,
  `item_pedido_saida_nome` VARCHAR(45) NOT NULL,
  `estoque_estoque_id` INT NOT NULL,
  PRIMARY KEY (`item_pedido_saida_id`),
  CONSTRAINT `fk_saida_item_pedido_saida1`
    FOREIGN KEY (`pedido_saida_pedido_saida_id`)
    REFERENCES `pedido_saida` (`pedido_saida_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_item_pedido_saida_estoque1`
    FOREIGN KEY (`estoque_estoque_id`)
    REFERENCES `estoque` (`estoque_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `movimentacao`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movimentacao` (
  `movimentacao_id` INT NOT NULL AUTO_INCREMENT,
  `movimentacao_tipo` VARCHAR(45) NOT NULL,
  `movimentacao_quantidade` INT NOT NULL,
  `movimentacao_data` VARCHAR(10) NOT NULL,
  `movimentacao_observacao` VARCHAR(50) NOT NULL,
  `item_pedido_entrada_item_pedido_entrada_id` INT NOT NULL,
  `item_pedido_saida_item_pedido_saida_id` INT NOT NULL,
  PRIMARY KEY (`movimentacao_id`),
  CONSTRAINT `fk_movimentacao_item_pedido_entrada1`
    FOREIGN KEY (`item_pedido_entrada_item_pedido_entrada_id`)
    REFERENCES `item_pedido_entrada` (`item_pedido_entrada_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_movimentacao_item_pedido_saida1`
    FOREIGN KEY (`item_pedido_saida_item_pedido_saida_id`)
    REFERENCES `item_pedido_saida` (`item_pedido_saida_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
