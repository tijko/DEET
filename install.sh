#!/usr/bin/env bash

for exe in $(ls)
do
    if [[ $exe =~ deet($|[^\.]) ]]
    then
        $(chmod 0777 $exe)
        $(mv $exe /usr/bin)
    fi
done

$(deet-makepkg)

$(cp deet.service /usr/lib/systemd/user/)
$(cp deet.timer /usr/lib/systemd/user/)

$(systemctl start deet.timer)
$(systemctl enable deet.timer)
$(systemctl daemon-reload)
