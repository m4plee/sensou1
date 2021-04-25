from django.shortcuts import render
from . import sensou


def str_card(card):
    path = []
    for _ in card:
        path.append(str(card[0]) + '_' + str(card[1] + '.png'))


ura_card = [(0, 'u')]


def game(request):
    if request.method == 'GET':
        is_gameover = False
        deck = sensou.Deck()
        cnt = 0
        player_get_num = 0
        com_get_num = 0
        plus = 0
        hand_num = 24 - int(cnt)

        request.session['deck'] = deck
        request.session['is_gameover'] = is_gameover

        d = {
            'message': '始めましょう！',
            'player_card': ['0_u.png'],
            'com_card': ['0_u.png'],
            'player_get_num': 0,
            'com_get_num': 0,
            'cnt': 0,
            'hands': ['0_u.png'] * hand_num
        }

        return render(request, 'game.html', d)

    else:
        deck = request.session['deck']
        is_gameover = request.session['is_gameover']

        player_card = [deck.emission()]
        com_card = [deck.emission()]

        if sensou.point(player_card) > sensou.point(com_card):
            player_get_num += 1 + plus
            cnt += 1
            plus = 0
            hand_num = 24 - int(cnt)
            deck = request.session['deck']
            is_gameover = request.session['is_gameover']
            d = {
                'message': 'プレイヤーに１ポイント入ります！',
                'player_card': ['str_card(player_card)'],
                'com_card': ['str_card(com_card)'],
                'player_get_num': player_get_num,
                'com_get_num': com_get_num,
                'cnt': cnt,
                'hands': ['0_u.png'] * hand_num,
            }
            return render(request, 'game.html', d)

        elif sensou.point(com_card) > sensou.point(player_card):
            com_get_num += 1 + plus
            cnt += 1
            hand_num = 24 - int(cnt)
            deck = request.session['deck']
            is_gameover = request.session['is_gameover']
            plus = 0
            d = {
                'message': 'NPCに１ポイント入ります！',
                'player_card': ['str_card(player_card)'],
                'com_card': ['str_card(com_card)'],
                'player_get_num': player_get_num,
                'com_get_num': com_get_num,
                'cnt': cnt,
                'hands': ['0_u.png',] * hand_num
            }
            return render(request, 'game.html', d)

        else:
            cnt += 1
            plus += 1
            hand_num = 24 - int(cnt)
            player_card = player_card.clear()
            com_card = com_card.clear()
            player_card = [deck.emission()]
            com_card = [deck.emission()]
            d = {
                'message': 'もう一度カードを選んでください',
                'player_card': ['str_card(player_card)'],
                'com_card': ['str_card(com_card)'],
                'player_get_num': player_get_num,
                'com_get_num': com_get_num,
                'cnt': cnt,
                'hands': ['0_u.png',] * hand_num
            }
            return render(request, 'game.html', d)
    if cnt == 26:
        is_gameover = True

        if player_get_num > com_get_num:
            msg = f'{player_get_num - com_get_num}ポイント差であなたの勝ちです！'
        elif com_get_num > player_get_num:
            msg = f'{com_get_num - player_get_num}ポイント差でNPCの勝ちです！'
        else:
            msg = '引き分けです！'

        d = {
            'message': msg,
            'player_card': ['str_card(player_card)'],
            'com_card': ['str_card(com_card)'],
            'player_get_num': player_get_num,
            'com_get_num': com_get_num,
            'cnt': cnt,
            'hands': ['0_u.png',] * hand_num
        }
