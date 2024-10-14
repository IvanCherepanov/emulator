.data
num 5
num 20
num 30
num 40
num 50
num 60
.code
LDA #0
STA /B
LDA @B
ADD #1
STA /C
LDA #1
STA /B
LDA #0
STA /A
LOOP:
LDA /B
LDA @B
ADD /A
STA /A
LDA /B
ADD #1
STA /B
LDA /B
CMP /C
JZ END
JMP LOOP
END:
HLT #0