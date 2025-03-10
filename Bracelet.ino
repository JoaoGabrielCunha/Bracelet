#include <SPI.h>
#define USE_SDFAT
#include <SdFat.h>
#include <Adafruit_GFX.h>
#include <MCUFRIEND_kbv.h>
#include <TouchScreen.h>
#include <JKSButton.h>




#define SD_CS 10
#define NAMEMATCH ""  // "" matches any name
//#define NAMEMATCH "tiger"    // *tiger*.bmp
#define PALETTEDEPTH 8  // support 256-colour Palette
#define BMPIMAGEOFFSET 54

#define BUFFPIXEL 20

//Parte da vibração
int motorPin = A10;                              // Pino PWM para o motor de vibração
unsigned long instante_anterior_millis = 0;      // Armazena o último tempo em que o motor foi atualizado
unsigned long instante_anterior_millis_som = 0;  // Armazena o istante anterior do som
unsigned long instante_anterior_millis_bat = 0;
bool motor_ligado = false;  // Estado do motor
int count = 0;
bool eh_para_vibrar = false;
int intensidade = 200;
int intervalo = 200;
int contagem_max = 3;








//Parte da tela//

JKSButton botao1, botao2, botao3, botao4;



// Parte da bateria
int tam_ret_atual;
int v_min;
int v_max;
int v_lido;





const int bat_pin = A8;  // Pino onde a bateria está armazenada
int sensor_bat = 0;      // Variável para armazenar o valor lido do sensor





//Parte da tela//

bool eh_para_desenhar = false;

char namebuf[32] = "/";  //Parte da imagem//
File root;
int pathlen;
SdFatSoftSpi<12, 11, 13> SD;
MCUFRIEND_kbv tela;

char *imagens[2];
char *nm;  //Parte da imagem//


// Parte sensor de som
const int sensorDeSom = 53;  // Pino onde o sensor de som está conectado
bool sensor_som = false;
//Função vibração


void vibra(int intensidade, int intervalo, int contagem_max) {
  unsigned long instante_atual_millis = millis();


  if (instante_atual_millis - instante_anterior_millis >= intervalo) {
    instante_anterior_millis = instante_atual_millis;

    if (count < contagem_max) {
      if (motor_ligado) {
        Serial.println("Motor desligado.");
        analogWrite(motorPin, 0);
        motor_ligado = false;
      } else {
        Serial.println("Motor ligado");
        analogWrite(motorPin, intensidade);
        motor_ligado = true;
        count++;
      }
    } else {
      Serial.println("Contagem máxima atingida, motor desligado permanentemente.");
      analogWrite(motorPin, 0);
      motor_ligado = false;
      eh_para_vibrar = false;
      count = 0;
    }
  }
}




//Funções da tela//
void mensagem_1(){
  Serial1.print("help");
}

void mensagem_2(){
  Serial1.print("comer");
}

void mensagem_3(){
  Serial1.print("banheiro");
}

void altera_som(){
  if(sensor_som== true){
    sensor_som = false;
  }
  else { sensor_som = true;  }
}



uint16_t read16(File &f) {
  uint16_t result;  // read little-endian
  f.read(&result, sizeof(result));
  return result;
}

uint32_t read32(File &f) {
  uint32_t result;
  f.read(&result, sizeof(result));
  return result;
}

uint8_t showBMP(char *nm, int x, int y) {
  File bmpFile;
  int bmpWidth, bmpHeight;          // W+H in pixels
  uint8_t bmpDepth;                 // Bit depth (currently must be 24, 16, 8, 4, 1)
  uint32_t bmpImageoffset;          // Start of image data in file
  uint32_t rowSize;                 // Not always = bmpWidth; may have padding
  uint8_t sdbuffer[3 * BUFFPIXEL];  // pixel in buffer (R+G+B per pixel)
  uint16_t lcdbuffer[(1 << PALETTEDEPTH) + BUFFPIXEL], *palette = NULL;
  uint8_t bitmask, bitshift;
  boolean flip = true;  // BMP is stored bottom-to-top
  int w, h, row, col, lcdbufsiz = (1 << PALETTEDEPTH) + BUFFPIXEL, buffidx;
  uint32_t pos;           // seek position
  boolean is565 = false;  //

  uint16_t bmpID;
  uint16_t n;  // blocks read
  uint8_t ret;

  if ((x >= tela.width()) || (y >= tela.height()))
    return 1;  // off screen

  bmpFile = SD.open(nm);             // Parse BMP header
  bmpID = read16(bmpFile);           // BMP signature
  (void)read32(bmpFile);             // Read & ignore file size
  (void)read32(bmpFile);             // Read & ignore creator bytes
  bmpImageoffset = read32(bmpFile);  // Start of image data
  (void)read32(bmpFile);             // Read & ignore DIB header size
  bmpWidth = read32(bmpFile);
  bmpHeight = read32(bmpFile);
  n = read16(bmpFile);                                         // # planes -- must be '1'
  bmpDepth = read16(bmpFile);                                  // bits per pixel
  pos = read32(bmpFile);                                       // format
  if (bmpID != 0x4D42) ret = 2;                                // bad ID
  else if (n != 1) ret = 3;                                    // too many planes
  else if (pos != 0 && pos != 3) ret = 4;                      // format: 0 = uncompressed, 3 = 565
  else if (bmpDepth < 16 && bmpDepth > PALETTEDEPTH) ret = 5;  // palette
  else {
    bool first = true;
    is565 = (pos == 3);  // ?already in 16-bit format
    // BMP rows are padded (if needed) to 4-byte boundary
    rowSize = (bmpWidth * bmpDepth / 8 + 3) & ~3;
    if (bmpHeight < 0) {  // If negative, image is in top-down order.
      bmpHeight = -bmpHeight;
      flip = false;
    }

    w = bmpWidth;
    h = bmpHeight;
    if ((x + w) >= tela.width())  // Crop area to be loaded
      w = tela.width() - x;
    if ((y + h) >= tela.height())  //
      h = tela.height() - y;

    if (bmpDepth <= PALETTEDEPTH) {  // these modes have separate palette
      bmpFile.seek(BMPIMAGEOFFSET);  //palette is always @ 54
      bitmask = 0xFF;
      if (bmpDepth < 8)
        bitmask >>= bmpDepth;
      bitshift = 8 - bmpDepth;
      n = 1 << bmpDepth;
      lcdbufsiz -= n;
      palette = lcdbuffer + lcdbufsiz;
      for (col = 0; col < n; col++) {
        pos = read32(bmpFile);  //map palette to 5-6-5
        palette[col] = ((pos & 0x0000F8) >> 3) | ((pos & 0x00FC00) >> 5) | ((pos & 0xF80000) >> 8);
      }
    }

    // Set TFT address window to clipped image bounds
    tela.setAddrWindow(x, y, x + w - 1, y + h - 1);
    for (row = 0; row < h; row++) {  // For each scanline...
      // Seek to start of scan line.  It might seem labor-
      // intensive to be doing this on every line, but this
      // method covers a lot of gritty details like cropping
      // and scanline padding.  Also, the seek only takes
      // place if the file position actually needs to change
      // (avoids a lot of cluster math in SD library).
      uint8_t r, g, b, *sdptr;
      int lcdidx, lcdleft;
      if (flip)  // Bitmap is stored bottom-to-top order (normal BMP)
        pos = bmpImageoffset + (bmpHeight - 1 - row) * rowSize;
      else  // Bitmap is stored top-to-bottom
        pos = bmpImageoffset + row * rowSize;
      if (bmpFile.position() != pos) {  // Need seek?
        bmpFile.seek(pos);
        buffidx = sizeof(sdbuffer);  // Force buffer reload
      }

      for (col = 0; col < w;) {  //pixels in row
        lcdleft = w - col;
        if (lcdleft > lcdbufsiz) lcdleft = lcdbufsiz;
        for (lcdidx = 0; lcdidx < lcdleft; lcdidx++) {  // buffer at a time
          uint16_t color;
          // Time to read more pixel data?
          if (buffidx >= sizeof(sdbuffer)) {  // Indeed
            bmpFile.read(sdbuffer, sizeof(sdbuffer));
            buffidx = 0;  // Set index to beginning
            r = 0;
          }
          switch (bmpDepth) {  // Convert pixel from BMP to TFT format
            case 24:
              b = sdbuffer[buffidx++];
              g = sdbuffer[buffidx++];
              r = sdbuffer[buffidx++];
              color = tela.color565(r, g, b);
              break;
            case 16:
              b = sdbuffer[buffidx++];
              r = sdbuffer[buffidx++];
              if (is565)
                color = (r << 8) | (b);
              else
                color = (r << 9) | ((b & 0xE0) << 1) | (b & 0x1F);
              break;
            case 1:
            case 4:
            case 8:
              if (r == 0)
                b = sdbuffer[buffidx++], r = 8;
              color = palette[(b >> bitshift) & bitmask];
              r -= bmpDepth;
              b <<= bmpDepth;
              break;
          }
          lcdbuffer[lcdidx] = color;
        }
        tela.pushColors(lcdbuffer, lcdidx, first);
        first = false;
        col += lcdidx;
      }                                                             // end cols
    }                                                               // end rows
    tela.setAddrWindow(0, 0, tela.width() - 1, tela.height() - 1);  //restore full screen
    ret = 0;                                                        // good render
  }
  bmpFile.close();
  return (ret);
}

void somDetectado() {
  if (sensor_som == true){
  unsigned long instanteAtual_som = millis();
  Serial.println("som!");
  if (instanteAtual_som > instante_anterior_millis_som + 10) {
    eh_para_desenhar = true;

    instante_anterior_millis_som = instanteAtual_som;
  }
}
}

void printWrappedText(MCUFRIEND_kbv &tela, int x, int y, int w, String text, uint16_t textColor, uint16_t bgColor) {
    int cursorX = x;
    int cursorY = y;
    tela.setTextColor(textColor, bgColor);
    
    String line = "";
    for (int i = 0; i < text.length(); i++) {
        line += text[i];
        int16_t x1, y1;
        uint16_t w1, h1;
        tela.getTextBounds(line, cursorX, cursorY, &x1, &y1, &w1, &h1);
        if (w1 > w) { // If the line width exceeds the box width, print the line and start a new one
            tela.setCursor(cursorX, cursorY);
            tela.print(line.substring(0, line.length() - 1));
            line = text[i];
            cursorY += h1;
        }
    }
    tela.setCursor(cursorX, cursorY);
    tela.print(line); // Print the last remaining line
}




void setup() {

  bool good = SD.begin(SD_CS); /*Inicia o arquivo SD */  //Desenha a imagem//
  if (!good) {
    Serial.print(F("cannot start SD"));
    while (1)
      ;
  }


  // Bateria

  v_min = 300;
  v_max = 735;

  Serial1.println("teste");

  //Fazendo o setup da vibração.
  pinMode(motorPin, OUTPUT);  //Iniciando o vibrador


  //Inicia a tela e o SD//
  uint16_t ID; /*Inicia o arquivo SD*/
  Serial.begin(9600);
  Serial1.begin(9600);
  ID = tela.readID();

  if (ID == 0x0D3D3) ID = 0x9481;
  tela.begin(ID);
 
  tela.setRotation(1);
  TouchScreen touch(6, A1, A2, 7, 300);
  tela.setTextColor(0xFFFF, 0x0000);  //Inicia a tela e o SD//

  showBMP("fundo_lua.bmp",0, 0);                                    // Fundo

  tela.drawRect(5, 21, 90, 150, TFT_BLACK);  // Imagem
  tela.fillRect(6, 22, 88, 148, 0xCE59);

  tela.drawRect(126, 21, 175, 150, TFT_BLACK);  // Texto
  tela.fillRect(127, 22, 173, 148, 0xCE59);

  tela.drawRect(245, 4, 55, 15, TFT_BLACK);  // Bateria
  tela.fillRect(246, 5, tam_ret_atual, 13, TFT_GREEN);

  //tela.fillRect(235, 0, 3, 3, TFT_BLACK);

  botao1.init(&tela, &touch, 30, 205, 54, 54, TFT_WHITE, 0x5B3B, TFT_BLACK, "Help", 1);
  botao1.setPressHandler(mensagem_1);

  botao2.init(&tela, &touch, 104, 205, 54, 54, TFT_WHITE, 0x5B3B, TFT_BLACK, "Comida", 1);
  botao2.setPressHandler(mensagem_2);

  botao3.init(&tela, &touch, 178, 205, 54, 54, TFT_WHITE, 0x5B3B, TFT_BLACK, "Banheiro", 1);
  botao3.setPressHandler(mensagem_3);

  botao4.init(&tela, &touch, 252, 205, 54, 54, TFT_WHITE, 0x5B3B, TFT_BLACK, "Sensor", 1);
  botao4.setPressHandler(altera_som);




  //showBMP("ok.bmp", 21, 61);  //Desenha a imagem//

  int origem = digitalPinToInterrupt(21);
  attachInterrupt(origem, somDetectado, RISING);
}

void loop() {
  botao1.process();
  botao2.process();
  botao3.process();
  botao4.process();


  if (eh_para_vibrar == true) {
    vibra(intensidade, intervalo, contagem_max);
  }





  if (Serial1.available() > 0) {
    eh_para_vibrar = true;  //Vibra e para

    String texto = Serial1.readStringUntil('\n');


    
    Serial.println(texto);
    texto.trim();
    //Serial.println("oi");

    int indice_espaco = texto.indexOf(' ');


    String nome_emoji = texto.substring(0, indice_espaco);
    String mensagem = texto.substring(indice_espaco + 1);


    char nome_emoji_char[32];
    nome_emoji.toCharArray(nome_emoji_char, 32);




    

    if (nome_emoji.endsWith(".bmp")) {
        // Chamar a função showBMP com nome_emoji_char se a mensagem contiver ".bmp"
        showBMP(nome_emoji_char, 6, 22);  // Desenha a imagem
    } else {
        // Preencher o quadrado de imagem com cinza se a mensagem não contiver ".bmp"
        tela.fillRect(6, 22, 88, 148, 0xCE59);  // 0x8410 é a cor cinza
    }


    tela.setTextSize(2);
    tela.setCursor(129, 24);

    tela.fillRect(127, 22, 173, 148,0xCE59);

    printWrappedText(tela, 128, 23, 173, mensagem, TFT_BLACK, 0xCE59);

    
    
  }

  


  unsigned long instanteAtual_bat = millis();

  if (instanteAtual_bat > instante_anterior_millis_bat + 5000) {

     delay(50);

    
    
   pinMode(bat_pin,INPUT);

    tam_ret_atual = 55 * (v_lido - v_min) / (v_max - v_min);
   
    

    tela.drawRect(246, 5, 55, 15, TFT_BLACK);  // Bateria
    tela.fillRect(246, 5, 55, 15, TFT_BLACK);
    tela.fillRect(246, 5, tam_ret_atual, 13, TFT_GREEN);
     instante_anterior_millis_bat = instanteAtual_bat;
  

  if(eh_para_desenhar== true){
    tela.setTextSize(2);
    tela.setCursor(127, 22);
    tela.fillRect(127, 22, 173, 148, 0xCE59);
    tela.setTextColor(TFT_BLACK);  // Ajuste a cor conforme necessário
    tela.print("Som detectado");
    showBMP("som.bmp", 6, 22);
    eh_para_desenhar = false;
  }

  }
}
