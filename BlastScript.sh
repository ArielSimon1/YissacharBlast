cat /home/stu/nissan/Yissachar-Blast/input_files/*.seq > /home/stu/nissan/Yissachar-Blast/check.txt
/private/software/bin/blastn -query /home/stu/nissan/Yissachar-Blast/check.txt? -db /private/db/nt/nt -out /home/stu/nissan/Yissachar-Blast/results.out
echo "level 3/3: print results:"
python3 /home/stu/nissan/Yissachar-Blast/blastn_checker.py /home/stu/nissan/Yissachar-Blast/results.out
# rm /home/stu/nissan/Yissachar-Blast/input_files/*