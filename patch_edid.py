import sys

def patch_edid(input_file, output_file, target_hz):
    with open(input_file, 'rb') as f:
        edid = bytearray(f.read())
    
    # DTD 1 Timings (Standard für dein Panel)
    h_active = 1920
    h_blank = 184 # 16+16+152
    v_active = 1080
    v_blank = 36  # 3+14+19
    
    h_total = h_active + h_blank
    v_total = v_active + v_blank
    
    # Berechne Pixeltakt für Ziel-Hz
    # Pixel Clock in Hz = H_total * V_total * Hz
    pixel_clock_hz = h_total * v_total * target_hz
    
    # EDID Spezifikation: Pixel Clock in 10 kHz Einheiten
    edid_clock = int(pixel_clock_hz / 10000)
    
    # Patch Clock (Little Endian) an Offset 54 und 55
    edid[54] = edid_clock & 0xFF
    edid[55] = (edid_clock >> 8) & 0xFF
    
    # Checksumme neu berechnen (Byte 127)
    edid[127] = 0 # Temporär auf 0 setzen
    new_checksum = (256 - (sum(edid[:128]) % 256)) % 256
    edid[127] = new_checksum
    
    with open(output_file, 'wb') as f:
        f.write(edid)
    
    print(f"Datei: {output_file}")
    print(f"Pixeltakt: {edid_clock * 10 / 1000:.2f} MHz")
    print(f"Checksumme: {hex(new_checksum)}")

patch_edid('original_edid.bin', 'overclock_90hz.bin', 90)
