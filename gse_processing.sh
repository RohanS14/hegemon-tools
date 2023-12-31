for i in phillips-2018-retina-expr.txt
do
    P=${i/-expr.txt/}
    echo $P
    rm -f "$P-thr.txt" "$P-info.txt" "$P-vinfo.txt" "$P-bv.txt"
    if [[ ! -f "$P-thr.txt" ]]; then
    perl -I /booleanfs/sahoo/scripts \
      /booleanfs/sahoo/scripts/absoluteInfo.pl thr \
      $i 2 70000 0.5 > "$P-thr.txt"
    fi
    if [[ ! -f "$P-info.txt" ]]; then
    perl -I /booleanfs/sahoo/scripts \
      /booleanfs/sahoo/scripts/hegemonutils.pl Info \
      $P > $P-info.txt
    fi
    if [[ ! -f "$P-vinfo.txt" ]]; then
    perl -I /booleanfs/sahoo/scripts \
      /booleanfs/sahoo/scripts/hegemonutils.pl VInfo \
      $P > $P-vinfo.txt
    fi
    if [[ ! -f "$P-bv.txt" ]]; then
    perl -I /booleanfs/sahoo/scripts \
      /booleanfs/sahoo/scripts/hegemonutils.pl bv \
      $P > $P-bv.txt
    fi
done

