#!/data/data/com.termux/files/usr/bin/bash
# Troca font.ttf para a próxima fonte da pasta (loop volta ao topo).
# Voltar à fonte original do git: git restore termux/font.ttf
cd "$(dirname "$(readlink -f "$0")")"

current=$(basename "$(readlink -f font.ttf)")
declare -a fonts=()
for f in *.ttf; do
  [ "$f" = "font.ttf" ] && continue
  fonts+=("$f")
done

n=${#fonts[@]}
next="${fonts[0]}"
for i in "${!fonts[@]}"; do
  if [ "${fonts[i]}" = "$current" ]; then
    next="${fonts[(( (i + 1) % n ))]}"  # (i+1) % n
    break
  fi
done

# rm é só do link, nunca da fonte
rm -f font.ttf
ln -sv "$next" font.ttf

termux-reload-settings

printf '\n%s\n' '========== TESTE DE FONTES =========='
printf '%s\n\n' "fonte atual: $current  (próxima: $next)"
printf '%s\n\n' 'Nerd Fonts | Legibilidade | Programação'

printf '%s\n' '--- 1. Alfabeto minúsculo ---'
printf '%s\n' 'abcdefghijklmnopqrstuvwxyz'
printf '%s\n' 'a b c d e f g h i j k l m n o p q r s t u v w x y z'
printf '%s\n\n' 'aaa ccc eee iii jjj mmm nnn ooo rrr uuu vvv www xxx'

printf '%s\n' '--- 2. Alfabeto maiúsculo ---'
printf '%s\n' 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
printf '%s\n' 'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'
printf '%s\n\n' 'CCC EEE ILL MMN OOO SSS UVW XYZ'

printf '%s\n' '--- 3. Letras e números parecidos ---'
printf '%s\n' '0 O o Q D'
printf '%s\n' '1 l I i | !'
printf '%s\n' '2 Z z'
printf '%s\n' '5 S s'
printf '%s\n' '6 G b'
printf '%s\n' '8 B'
printf '%s\n' 'rn m'
printf '%s\n' 'vv w'
printf '%s\n' 'cl d'
printf '%s\n' 'li h'
printf '%s\n\n' 'Il1|I1l|0OoQ|5S5S|rnrm|vvvw'

printf '%s\n' '--- 4. Letras com números ---'
printf '%s\n' 'abc123'
printf '%s\n' 'ABC123'
printf '%s\n' 'foo0 bar1 baz2'
printf '%s\n' 'O0 OO 00 o0 0o'
printf '%s\n' 'l1I lIl 1lI I1l'
printf '%s\n\n' 'user_id userId USER_ID user-id'

printf '%s\n' '--- 5. Aspas e espaços ---'
printf '%s\n' "a"
printf '%s\n' "'a'"
printf '%s\n' '"a"'
printf '%s\n' "''"
printf '%s\n' '""'
printf '%s\n' "' '"
printf '%s\n' '" "'
printf '%s\n' "'  '"
printf '%s\n' '"  "'
printf '%s\n' "'   '"
printf '%s\n' '"   "'
printf '%s\n' "' 0 '"
printf '%s\n' '" 0 "'
printf '%s\n' "don't"
printf '%s\n' 'it'"'"'s'
printf '%s\n\n' 'He said: "hello"'

printf '%s\n' '--- 6. Pontuação ---'
printf '%s\n' '. , : ; ! ?'
printf '%s\n' "' \" \`"
printf '%s\n' '_ - -- ---'
printf '%s\n' '... .. .'
printf '%s\n' ';; :: ,,,'
printf '%s\n' '!? !! ??'
printf '%s\n\n' '... --- ...'

printf '%s\n' '--- Operadores: comparação ---'
printf '%s\n' '<  >  <=  >='
printf '%s\n' '==  !=  ===  !=='
printf '%s\n' '<=  =<  >=  =>'
printf '%s\n' '≠  ≤  ≥  ≈  ≡'
printf '%s\n\n' 'a < b | a <= b | a > b | a >= b'

printf '%s\n' '--- Operadores: deslocamento e bits ---'
printf '%s\n' '<  <<  <<<  <<=  <<='
printf '%s\n' '>  >>  >>>  >>=  >>>='
printf '%s\n' '&  &&  &=  |  ||  |='
printf '%s\n' '^  ^=  ~  !  !!'
printf '%s\n\n' 'x << 1 | x >> 1 | x >>> 1'

printf '%s\n' '--- Operadores: atribuição ---'
printf '%s\n' '=  :=  +=  -=  *=  /='
printf '%s\n' '%=  &=  |=  ^=  <<=  >>='
printf '%s\n' '**=  //=  ??=  &&=  ||='
printf '%s\n\n' 'x = y | x == y | x === y'

printf '%s\n' '--- Operadores: setas ---'
printf '%s\n' '->  -->  --->  ->>'
printf '%s\n' '<-  <--  <---  <<-'
printf '%s\n' '=>  ==>  ===>  =>>'
printf '%s\n' '<=  <==  <===  <==>'
printf '%s\n' '<->  <-->  <=>  <==>'
printf '%s\n\n' 'a -> b | a => b | a --> b'

printf '%s\n' '--- Operadores: aritmética ---'
printf '%s\n' '+  -  *  /  %  **  //'
printf '%s\n' '++  --  +=  -=  *=  /='
printf '%s\n' 'a+b  a-b  a*b  a/b  a%b'
printf '%s\n\n' '2**3  7//2  x++  --y'

printf '%s\n' '--- Operadores: nulos e condicionais ---'
printf '%s\n' '?  ??  ?.  ?:  !!  !'
printf '%s\n' '&&  ||  and  or  not'
printf '%s\n' 'x ?? y | x?.name | x != null'
printf '%s\n\n' 'condition ? value1 : value2'

printf '%s\n' '--- Operadores: dois ou mais caracteres ---'
printf '%s\n' '::  :::  :=  :>'
printf '%s\n' '..  ...  ..<  ...>'
printf '%s\n' '.*  ->*  .*  ::*'
printf '%s\n' '==  ===  ====  !=  !=='
printf '%s\n' '&&  &&&  ||  |||'
printf '%s\n\n' '<<=  >>=  **=  ??=  <=>'

printf '%s\n' '--- Operadores: comparação visual ---'
printf '%s\n' '<>  ><  <=  =<  >=  =>'
printf '%s\n' '<<  >>  < <  > >'
printf '%s\n' '->  - >  =>  = >'
printf '%s\n' '==  = =  ===  = =='
printf '%s\n' '!=  ! =  !==  ! =='
printf '%s\n' '...  ..  . .  ::  : :'
printf '%s\n\n' '&&  & &  ||  | |'

printf '%s\n' '--- 7. Números e sistema numérico ---'
printf '%s\n' '0 1 2 3 4 5 6 7 8 9'
printf '%s\n' '0123456789  1029384756  0011223344'
printf '%s\n' 'hex:  0x0F 0x1A 0xFF 0xAB20 0x9A3E  41 42 43'
printf '%s\n' 'bin:  0b1011_0101  0b1111_0000  0b1010 0o755'
printf '%s\n' 'dec:  00 10 25 50 75 99  100 250 1000'
printf '%s\n\n' 'l1 I1 0O 5S B8 2Z 6G 9g'

printf '%s\n' '--- 8. Acentos (pt-BR) e símbolos ---'
printf '%s\n' 'Á É Í Ó Ú Â Ê Ô Ã Õ À Ç'
printf '%s\n' 'á é í ó ú â ê ô ã õ à ç'
printf '%s\n' 'maçã  ação  ônibus  pé  ácido  íntegro  órfão  Úden'
printf '%s\n' 'nº 3ª 2º  ¢ € µ ± ° ¹ ² ³  «aspas» – dash — travessão'
printf '%s\n\n' 'não  dão  vão  pão  mão  são'

printf '%s\n' '--- 9. Ícones do nvim-tree e devicons ---'
printf '%b\n' 'folder:    \ue5fe \ue5ff \uf115'
printf '%b\n' 'file:      \U000F021A'
printf '%b\n' 'symlink:   \U000F0338'
printf '%b\n' 'git:       \uf4a3'
printf '%b\n' 'python:\ue73b  js:\ue74e  lua:\ue620  json:\ue60b'
printf '%b\n' 'css:\ue749  yaml:\ue8eb  vim:\ue62b  shell:\ue795'
printf '%b\n' 'docker:\ue650  react:\ue7ba  tsx:\ue7bc  check:\ue5fb'
printf '%b\n\n' '\ue73b\ue74e\ue620\ue60b\ue749\ue8eb\ue62b\ue795\ue650\ue7ba\ue7bc\ue5fb (dense: olhe o corte)'

printf '%s\n' '--- 10. Box drawing, powerline e blocos ---'
printf '%s\n' '═ ║ ╔ ╗ ╚ ╝ ╠ ╣  ─ │ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼'
printf '%s\n' '░ ▒ ▓ █ ▀ ▄ ▖ ▗ ▘ ▙ ▚ ▛'
printf '%b\n' 'powerline: \ue0b0 \ue0b2 \ue0b4 \ue0b6 \ue0ba \ue0bc \ue0c0 \ue0c4'
printf '%b\n\n' '\ue725 [plugin] \uf021a [buf]  ok err warn info'

printf '%s\n' '--- 11. Casos Especificos ---'
echo '~-= ~/'
