import calendar
from datetime import datetime, timedelta, date
import math
import time

jumlah_cuti_kantor = 14
jumlah_cuti_bersama = int(input("jumlah cuti bersama = "))
tanggal_join_karyawan = str(input("tanggal join karyawan = "))
tanggal_rencana_cuti = str(input("tanggal rencana cuti = "))
durasi_cuti = int(input("durasi cuti (hari) = "))
cuti_pribadi = jumlah_cuti_kantor - jumlah_cuti_bersama

reason = []
if durasi_cuti > 3:
    reason.append("cuti maksimal hanya 3 hari")

object_tanggal_join_karyawan = datetime.strptime(tanggal_join_karyawan, "%Y-%m-%d")
object_tanggal_rencana_cuti = datetime.strptime(tanggal_rencana_cuti, "%Y-%m-%d")
tanggal_bisa_ambil_cuti = object_tanggal_join_karyawan + timedelta(days = 180)
end_of_year_date = date(int(tanggal_bisa_ambil_cuti.strftime("%Y")),12 ,31)

available_jumlah_cuti_raw_days = end_of_year_date - tanggal_bisa_ambil_cuti.date()
available_cuti = math.floor(available_jumlah_cuti_raw_days.days / 365 * cuti_pribadi)

object_tanggal_rencana_cuti = datetime.strptime(tanggal_rencana_cuti, "%Y-%m-%d")


if durasi_cuti > available_cuti:
    reason.append("hanya boleh mengambil " + str(available_cuti) + " hari cuti")

if object_tanggal_rencana_cuti < tanggal_bisa_ambil_cuti:
    reason.append("belum 180 hari sejak tanggal join karyawan")


if len(reason) > 0:
    print(False)
    for i in reason:
        print(i)
    quit()

print(True)
