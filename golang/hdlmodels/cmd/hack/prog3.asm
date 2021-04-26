(INICIO)        
        @4       // carga A con 3
        D=A      // D = 3
(HERE)        
        @HERE
        D=D-1;JNE
        @INICIO  // carga A con INICIO
        0;JMP    // salta a     INICIO