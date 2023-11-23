# postos
# https://www.bcb.gov.br/fis/info/cad/postos/202310POSTOS.zip

library(tidyverse)
caminho_do_diretorio <- "data/zip"

# Use dir.create() para criar o diretório
if (!file.exists(caminho_do_diretorio)) {
  dir.create(caminho_do_diretorio, recursive = TRUE)
  cat("Diretório criado com sucesso.\n")
} else {
  cat("O diretório já existe.\n")
}

anos <- 2023
mes <- c("01","02","03","04","05","06","07","08","09",10,11,12) 
partes_finais_url <- expand.grid(anos,mes) %>% 
  mutate(anomes= paste0(Var1,Var2,"POSTOS")) %>% 
  pull(anomes)

# Crie um diretório temporário
# Loop sobre as partes finais do URL
for (parte_final_url in partes_finais_url) {
  # Construa a URL completa
  url <- paste0("https://www.bcb.gov.br/fis/info/cad/postos/", parte_final_url, ".zip")
  
  # Combine o diretório temporário com o nome do arquivo zip
  caminho_local <- file.path(caminho_do_diretorio, paste0(parte_final_url, ".zip"))
  
  # Use a função download.file para baixar o arquivo zip
  download.file(url, caminho_local, mode = "wb")
  
  # Verifique se o download foi bem-sucedido
  if (file.exists(caminho_local)) {
    cat("Download concluído com sucesso. O arquivo está em:", caminho_local, "\n")
  } else {
    cat("Erro ao baixar o arquivo.\n")
  }
}

list.files(path = caminho_do_diretorio,
           pattern = "*.zip",
           full.names = TRUE)  %>% 
  walk(~ unzip(.,exdir = "data/zip/"))

my_tbl <- list.files(path = "./data/zip",
                     pattern =  "*.xlsx",
                     full.names = TRUE) %>%
  map_df(~readxl::read_excel(., skip = 9))

do.call(file.remove, 
        list(list.files(path = here::here("data","zip"), 
                        full.names = TRUE)))
saveRDS(my_tbl,file = here::here("data","raw","postos.RDS"))  






