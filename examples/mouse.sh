waykey mouse_move 100 300 -a
for ((i = 3 ; i < 7 ; i++)); do
    waykey mouse_move 100 $((i * 100)) -a
    for ((j = 0 ; j < 10 ; j++)); do
        waykey mouse_move 100 0
        sleep 0.05
    done
done
