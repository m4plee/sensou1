from django.shortcuts import render
from . import sensou


def card_path(cards):
    path = []
    for card in cards:
        path.append(str(card[0]) + '_' + str(card[1]) + '.png')
    return path


def point(card):
    tup = card[0]
    point = tup[0]
    if point == 1:
        return 14
    else:
        return point


def game(request):
    if request.method == 'GET' or 'restart' in request.POST:
        is_gamestart = True
        is_gameover = False
        deck = sensou.Deck()
        game_cnt = 0
        player_get_num = 0
        com_get_num = 0
        plus = 0
        hand_num = 26 - int(game_cnt)
        win_get_num = 0
        is_turn = False

        request.session['deck'] = deck
        request.session['is_gamestart'] = is_gamestart
        request.session['is_gameover'] = is_gameover
        request.session['plus'] = plus
        request.session['player_get_num'] = player_get_num
        request.session['com_get_num'] = com_get_num
        request.session['game_cnt'] = game_cnt
        request.session['win_get_num'] = win_get_num
        request.session['is_turn'] = is_turn

        d = {
            'message': '始めましょう！',
            'player_card': ['0_u.png'],
            'com_card': ['0_u.png'],
            'player_get_num': 0,
            'com_get_num': 0,
            'hands': ['0_u.png'] * hand_num,
            'is_gamestart': is_gamestart,
            'is_turn': is_turn,
        }

        return render(request, 'game.html', d)

    if request.method == 'POST':
        is_gamestart = False
        is_turn = True
        plus = request.session['plus']
        deck = request.session['deck']
        player_get_num = request.session['player_get_num']
        com_get_num = request.session['com_get_num']
        game_cnt = request.session['game_cnt']
        is_gameover = request.session['is_gameover']
        win_get_num = request.session['win_get_num']
        request.session['is_turn'] = is_turn

        if 'your' in request.POST:
            game_cnt = request.session['game_cnt']
            win_get_num = request.session['win_get_num']
            is_gameover = request.session['is_gameover']
            is_turn = request.session['is_turn']
            if game_cnt == 26:
                player_get_num = request.session['player_get_num']
                com_get_num = request.session['com_get_num']
                is_gamestart = request.session['is_gamestart']
                request.session['is_gamestart'] = is_gamestart
                player_card = request.session['player_card']
                com_card = request.session['com_card']
                is_gameover = True
                request.session['is_gameover'] = is_gameover
                is_turn = False

                if player_get_num > com_get_num:
                    is_gameover = request.session['is_gameover']
                    msg = f'{player_get_num - com_get_num}ポイント差であなたの勝ちです！'
                elif com_get_num > player_get_num:
                    is_gameover = request.session['is_gameover']
                    msg = f'{com_get_num - player_get_num}ポイント差でNPCの勝ちです！'
                else:
                    is_gameover = request.session['is_gameover']
                    msg = '引き分けです！'

                d = {
                    'message': msg,
                    'player_card': card_path(player_card),
                    'com_card': card_path(com_card),
                    'player_get_num': player_get_num,
                    'com_get_num': com_get_num,
                    'hands': ['0_u.png'] * 0,
                    'is_gameover': is_gameover,
                    'is_turn': is_turn,
                }
                return render(request, 'game.html', d)

            else:
                player_card = [deck.emission()]
                com_card = [deck.emission()]
                plus = request.session['plus']
                deck = request.session['deck']
                game_cnt = request.session['game_cnt']
                player_get_num += 0
                com_get_num += 0
                is_turn = request.session['is_turn']

                if point(player_card) > point(com_card):
                    deck = request.session['deck']
                    plus = request.session['plus']
                    win_get_num = request.session['win_get_num']
                    game_cnt = request.session['game_cnt']
                    is_turn = request.session['is_turn']

                    win_get_num += 1
                    com_get_num += 0
                    game_cnt += 1
                    plus += 1
                    player_get_num += plus
                    hand_num = 26 - int(game_cnt)

                    request.session['deck'] = deck
                    request.session['is_gamestart'] = is_gamestart
                    request.session['is_gameover'] = is_gameover
                    request.session['plus'] = plus
                    request.session['player_get_num'] = player_get_num
                    request.session['com_get_num'] = com_get_num
                    request.session['game_cnt'] = game_cnt
                    request.session['is_turn'] = is_turn

                    d = {
                        'message': f'プレイヤーに{plus}ポイント入ります！',
                        'player_card': card_path(player_card),
                        'com_card': card_path(com_card),
                        'player_get_num': player_get_num,
                        'com_get_num': com_get_num,
                        'hands': ['0_u.png'] * hand_num,
                        'is_turn': is_turn,
                    }
                    plus = 0
                    request.session['plus'] = plus
                    win_get_num = 0
                    request.session['win_get_num'] = win_get_num
                    if game_cnt == 26:
                        request.session['player_card'] = player_card
                        request.session['com_card'] = com_card
                        return render(request, 'game.html', d)

                    else:
                        player_card = list(player_card)
                        player_card.clear()
                        com_card = list(com_card)
                        com_card.clear()
                        request.session['game_cnt'] = game_cnt
                        return render(request, 'game.html', d)

                elif point(com_card) > point(player_card):
                    deck = request.session['deck']
                    plus = request.session['plus']
                    win_get_num = request.session['win_get_num']
                    game_cnt = request.session['game_cnt']
                    is_turn = request.session['is_turn']

                    game_cnt += 1
                    hand_num = 26 - int(game_cnt)
                    win_get_num += 1
                    player_get_num += 0
                    plus += 1
                    com_get_num += plus

                    request.session['deck'] = deck
                    request.session['is_gamestart'] = is_gamestart
                    request.session['is_gameover'] = is_gameover
                    request.session['plus'] = plus
                    request.session['player_get_num'] = player_get_num
                    request.session['com_get_num'] = com_get_num
                    request.session['game_cnt'] = game_cnt
                    request.session['is_turn'] = is_turn

                    d = {
                        'message': f'NPCに{plus}ポイント入ります！',
                        'player_card': card_path(player_card),
                        'com_card': card_path(com_card),
                        'player_get_num': player_get_num,
                        'com_get_num': com_get_num,
                        'hands': ['0_u.png'] * hand_num,
                        'is_turn': is_turn,
                    }
                    plus = 0
                    win_get_num = 0
                    request.session['plus'] = plus
                    request.session['win_get_num'] = win_get_num
                    if game_cnt == 26:
                        request.session['player_card'] = player_card
                        request.session['com_card'] = com_card
                        return render(request, 'game.html', d)
                    else:
                        player_card = list(player_card)
                        player_card.clear()
                        com_card = list(com_card)
                        com_card.clear()
                        request.session['game_cnt'] = game_cnt
                        return render(request, 'game.html', d)

                else:
                    deck = request.session['deck']
                    plus = request.session['plus']
                    win_get_num = request.session['win_get_num']
                    game_cnt = request.session['game_cnt']
                    is_turn = request.session['is_turn']

                    game_cnt += 1
                    plus += 1
                    hand_num = 26 - int(game_cnt)
                    win_get_num += 1

                    request.session['deck'] = deck
                    request.session['is_gamestart'] = is_gamestart
                    request.session['is_gameover'] = is_gameover
                    request.session['plus'] = plus
                    request.session['player_get_num'] = player_get_num
                    request.session['com_get_num'] = com_get_num
                    request.session['game_cnt'] = game_cnt
                    request.session['is_turn'] = is_turn

                    d = {
                        'message': '引き分けです！もう一度！',
                        'player_card': card_path(player_card),
                        'com_card': card_path(com_card),
                        'player_get_num': player_get_num,
                        'com_get_num': com_get_num,
                        'hands': ['0_u.png'] * hand_num,
                        'is_turn': is_turn,
                    }
                    request.session['plus'] = plus
                    request.session['win_get_num'] = win_get_num

                    if game_cnt == 26:
                        request.session['player_card'] = player_card
                        request.session['com_card'] = com_card
                        return render(request, 'game.html', d)
                    else:
                        player_card = list(player_card)
                        player_card.clear()
                        com_card = list(com_card)
                        com_card.clear()
                        request.session['game_cnt'] = game_cnt
                        request.session['is_turn'] = is_turn
                        return render(request, 'game.html', d)
