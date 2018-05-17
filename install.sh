#!/usr/bin/env bash

for exe in $(ls)
do
    if [[ $exe =~ deet($|[^\.]) ]]
    then
        $(chmod 0777 $exe)
        $(cp $exe /usr/bin)
    fi
done


$(cp deet.service /usr/lib/systemd/system/)
$(cp deet.timer /usr/lib/systemd/system/)

$(systemctl daemon-reload)
$(systemctl enable deet.timer)
$(systemctl start deet.timer)


if [[ $? -ne 0 ]]
then
    echo Error deploying deet service!
    exit 1
fi

$(deet-makepkg)
$(rm makepkg*)
