rule flag_format {
    strings:
        $regex_string = /ctf4b{.+}/
    condition:
        $regex_string
}
rule flag_size {
    condition:
       filesize == 36
}
rule maybe_flag {
    condition:
       flag_format and flag_size
}