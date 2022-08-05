#!/bin/sh
yesterday="@$(($(date +%s) - 86400))"
formatDate="%Y_%m_%d_%s"
date -d $yesterday +$formatDate
