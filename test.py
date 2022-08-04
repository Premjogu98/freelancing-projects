main = """Produced by
elementz & jae5
written by
elementz, jae5 & burna boy
additional vocals
jae5, keven wolfshon, kwande bawa, paul bohumil goller & uncle t
assistant mixing engineer
mixgiant & joe begalla
mixing engineer
jesse ray ernster
mastering engineer
gerhard west phalen
recording engineer
eric issac utere
a&r administrator
irene sourlis
a&r coordinator
spaceship collective & matthew baus
copyright ©
on a spaceship records, bad habit records & atlantic records
phonographic copyright ℗
on a spaceship records, bad habit records & atlantic records
label
on a spaceship records, bad habit records & atlantic records
distributor
atlantic records
release date
july 8, 2022"""
info_list = main.split("\n")
print(info_list)
while len(info_list) != 0:
    print(info_list[0],":",info_list[1])
    del info_list[0]
    del info_list[0]
    # print(info_list)