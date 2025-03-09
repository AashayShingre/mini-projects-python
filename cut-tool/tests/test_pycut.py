from app import pycut
import subprocess


def compare_commands(command1, command2):
    result1 = subprocess.run(command1, shell=True, capture_output=True, text=True)
    result2 = subprocess.run(command2, shell=True, capture_output=True, text=True)
    assert result1.stdout == result2.stdout


def test_cut1():
    compare_commands("cut -w -f3-4 sample.txt", "pycut -w -f3-4 sample.txt")


def test_step1():
    compare_commands("cut -f2 sample.csv", "pycut -f2 sample.csv")


def test_step2():
    compare_commands(
        "cut -f1 -d, sample.csv | head -n5", "pycut -f1 -d, sample.csv | head -n5"
    )


def test_step3():
    compare_commands("cut -f1,2 sample.csv", "pycut -f1,2 sample.csv")


def test_step4():
    compare_commands(
        'tail -n5 sample.csv | cut -d, -f"1 2"',
        'tail -n5 sample.csv | pycut -d, -f"1 2"',
    )


def test_step5():
    compare_commands(
        "cut -f2 -d, sample.csv | uniq | wc -l",
        "pycut -f2 -d, sample.csv | uniq | wc -l",
    )
