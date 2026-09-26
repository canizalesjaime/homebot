from stl import mesh, Mode
import sys

def convert_to_stl_ascii(stl_file):
    part = mesh.Mesh.from_file(stl_file)
    part.save(stl_file[:len(stl_file)-4]+"_ascii.stl",mode=Mode.ASCII)


def main():
    if len(sys.argv) == 2:
        print(sys.argv)
        convert_to_stl_ascii(sys.argv[1])

    else:
        print("incorrect # of command line arguments")


if __name__=="__main__":
    main()