    if game_state == "start_screen":
        screen.fill((172, 147, 98))
        title_surf = title_font.render(
            "Save the LaLas!", True, (255, 255, 255))
        instr_surf = instr_font.render(
            "Click Enter oder Space to start...", True, (200, 200, 200))
        screen.blit(
            title_surf, ((width - title_surf.get_width())//2, height//3))
        screen.blit(
            instr_surf, ((width - instr_surf.get_width())//2, height//3 + 100))
        pygame.display.update()
        clock.tick(60)
        continue

    if game_state == "intro":
        screen.blit(lala_img, lala_rect)
        screen.blit(player, player_rect)
        if dialogue_index < len(text_renders):
            text_surface = text_renders[dialogue_index]
            padding = 12
            panel_w = text_surface.get_width() + padding * 2
            panel_h = text_surface.get_height() + padding * 2
            panel = pygame.transform.smoothscale(panel_img, (panel_w, panel_h))
            panel.blit(text_surface, (padding, padding))
            panel_x = (width - panel_w) // 2
            panel_y = height - panel_h - 20
            screen.blit(panel, (panel_x, panel_y))
        pygame.display.update()
        clock.tick(60)
        continue

    if game_state == "postfight_dialogue":
        screen.blit(scorpion_img, scorpion_rect)
        screen.blit(player, player_rect)
        if dialogue_index < len(postfight_dialogue):
            text_surface = text_renders[dialogue_index] if dialogue_index < len(text_renders) else font.render(postfight_dialogue[dialogue_index], True, (172, 147, 98))
            padding = 12
            panel_w = text_surface.get_width() + padding * 2
            panel_h = text_surface.get_height() + padding * 2
            panel = pygame.transform.smoothscale(panel_img, (panel_w, panel_h))
            panel.blit(text_surface, (padding, padding))
            panel_x = (width - panel_w) // 2
            panel_y = height - panel_h - 20
            screen.blit(panel, (panel_x, panel_y))
        pygame.display.update()
        clock.tick(60)
        continue

    if game_state == "scorpion_fight":
        screen.blit(desert_bg, (0, 0))
        if scorpion_active:
            screen.blit(scorpion_img, scorpion_rect)
        screen.blit(player, player_rect)
        
        # Scorpion Attacken rendern
        for p in poison_spews:
            screen.blit(poison_img, p['rect'])
        
        # Messer und Spikes rendern
        for k in knives:
            screen.blit(knife_img, k['rect'])
        for s in spikes:
            screen.blit(spike_img, s['rect'])
        
        # Gegenstände rendern
        for item in dropped_items:
            screen.blit(item['img'], item['rect'])
        
        # Leben anzeigen
        for i in range(player_lives):
            x = 10 + i * (heart_img.get_width() + 5)
            y = 10
            screen.blit(heart_img, (x, y))
        
        # Skorpion Leben Anzeige
        if scorpion_active:
            bar_w = scorpion_img.get_width()
            bar_h = 6
            bar_x = scorpion_rect.left
            bar_y = scorpion_rect.top - bar_h - 4
            if bar_w > 0:
                health_ratio = scorpion_lives / float(rooms[current_room].get("scorpion_lives", max(1, scorpion_lives)))
                pygame.draw.rect(screen, (120, 120, 120), (bar_x, bar_y, bar_w, bar_h))
                pygame.draw.rect(screen, (200, 50, 50), (bar_x, bar_y, int(bar_w * health_ratio), bar_h))
        
        render_inventory(screen, mouse_pos, equipped_index)
        pygame.display.update()
        clock.tick(60)
        continue

    if game_state == "forest":
        screen.blit(forest_bg, (0, 0))
        screen.blit(player, player_rect)
        
        # Bäume rendern
        for t in trees:
            if t.get('img') is not None:
                screen.blit(t['img'], t['rect'])
        
        # Messer rendern
        for k in knives:
            screen.blit(knife_img, k['rect'])
        
        # Gegenstände rendern
        for item in dropped_items:
            screen.blit(item['img'], item['rect'])
        
        # Holz-Zähler anzeigen
        wood_count = count_item_in_inventory(ITEM_WOOD)
        wood_text = font.render(f"Holz: {wood_count}/8", True, (255, 255, 255))
        screen.blit(wood_text, (10, 50))
        
        # Wenn genug Holz: Nachricht zum Ufer gehen
        if wood_count >= 8:
            msg = font.render("Du hast genug Holz! Gehe zum Ufer (rechts)", True, (100, 200, 100))
            screen.blit(msg, (width // 2 - msg.get_width() // 2, 50))
        
        # Leben anzeigen
        for i in range(player_lives):
            x = 10 + i * (heart_img.get_width() + 5)
            y = height - 70
            screen.blit(heart_img, (x, y))
        
        render_inventory(screen, mouse_pos, equipped_index)
        
        if is_crafting_open:
            craft_button_rect, raft_button_rect = display_crafting_panel(screen)
        
        pygame.display.update()
        clock.tick(60)
        continue

    if game_state == "raft_building":
        screen.blit(island_bg, (0, 0))
        
        # Wasser zeichnen
        pygame.draw.rect(screen, (40, 100, 200), pygame.Rect(0, 600, width, height - 600))
        
        screen.blit(player, player_rect)
        
        # Gegenstände rendern
        for item in dropped_items:
            screen.blit(item['img'], item['rect'])
        
        # Floß-Bau-Menü
        if not raft_building_active:
            msg = font.render("Drücke R um das Floß zu bauen", True, (255, 255, 255))
            screen.blit(msg, (width // 2 - msg.get_width() // 2, 100))
            
            wood_count = count_item_in_inventory(ITEM_WOOD)
            resin_count = count_item_in_inventory(ITEM_RESIN)
            wood_text = font.render(f"Holz: {wood_count}/4", True, (200, 200, 200))
            resin_text = font.render(f"Harz: {resin_count}/3", True, (200, 200, 200))
            screen.blit(wood_text, (width // 2 - 100, 150))
            screen.blit(resin_text, (width // 2 - 100, 180))
            
            if wood_count >= 4 and resin_count >= 3:
                ready_msg = font.render("Floß gebaut! Drücke SPACE um zu starten", True, (100, 200, 100))
                screen.blit(ready_msg, (width // 2 - ready_msg.get_width() // 2, 220))
        
        # Leben anzeigen
        for i in range(player_lives):
            x = 10 + i * (heart_img.get_width() + 5)
            y = 10
            screen.blit(heart_img, (x, y))
        
        render_inventory(screen, mouse_pos, equipped_index)
        pygame.display.update()
        clock.tick(60)
        continue

    if game_state == "boss_fight":
        screen.blit(island_bg, (0, 0))
        
        # Wasser
        pygame.draw.rect(screen, (40, 100, 200), pygame.Rect(0, 600, width, height - 600))
        
        screen.blit(player, player_rect)
        if boss_active:
            screen.blit(lulu_img, boss_rect)
        
        # Messer rendern
        for k in knives:
            screen.blit(knife_img, k['rect'])
        
        # Boss Attacken rendern
        for p in poison_spews:
            screen.blit(poison_img, p['rect'])
        
        # Boss Leben anzeigen
        if boss_active:
            bar_w = 200
            bar_h = 20
            bar_x = (width - bar_w) // 2
            bar_y = 50
            pygame.draw.rect(screen, (120, 120, 120), (bar_x, bar_y, bar_w, bar_h))
            health_ratio = boss_lives / float(boss_max_lives)
            pygame.draw.rect(screen, (200, 50, 50), (bar_x, bar_y, int(bar_w * health_ratio), bar_h))
            boss_text = font.render(f"Lulu (Boss): {boss_lives}/{boss_max_lives}", True, (255, 255, 255))
            screen.blit(boss_text, (bar_x - 100, bar_y - 30))
        
        # Wenn Boss besiegt
        if boss_lives <= 0:
            boss_active = False
            victory_text = title_font.render("Du hast gewonnen!", True, (100, 200, 100))
            screen.blit(victory_text, (width // 2 - victory_text.get_width() // 2, height // 2))
            pygame.display.update()
            clock.tick(60)
            time.sleep(3)
            reset_game_state()
            continue
        
        # Leben anzeigen
        for i in range(player_lives):
            x = 10 + i * (heart_img.get_width() + 5)
            y = 10
            screen.blit(heart_img, (x, y))
        
        render_inventory(screen, mouse_pos, equipped_index)
        pygame.display.update()
        clock.tick(60)
        continue

    if game_state == "main":
        if lala_alive and rooms[current_room]["has_lala"]:
            screen.blit(lala_img, lala_rect)
                        
        for wrect in water_rects:
            pygame.draw.rect(screen, (40, 100, 200), wrect)

        for r in raft_objects:
            pygame.draw.rect(screen, (120, 70, 30), r['rect'])
            screen.blit(plank_img, r['rect'])

        for t in trees:
            if t.get('img') is not None:
                screen.blit(t['img'], t['rect'])

        if scorpion_active:
            if random.random() < 0.01:
                sx, sy = scorpion_rect.center
                px, py = player_rect.center
                dx = px - sx
                dy = py - sy
                dist = (dx*dx + dy*dy) ** 0.5
                if dist == 0:
                    dist = 1
                vx = (dx / dist) * poison_speed
                vy = (dy / dist) * poison_speed
                p = {
                    'x': sx - poison_img.get_width() / 2,
                    'y': sy - poison_img.get_height() / 2,
                    'vx': vx,
                    'vy': vy,
                    'rect': poison_img.get_rect(center=(int(sx), int(sy)))
                }
                poison_spews.append(p)

    # knife mechanics
        for k in knives[:]:
            k['rect'].x += k['vx']
            if k['rect'].right < 0 or k['rect'].left > width:
                knives.remove(k)
                continue
            if lala_alive and k['rect'].colliderect(lala_rect):
                lala_lives = max(0, lala_lives - 1)
                knives.remove(k)
                continue
            if scorpion_active and k['rect'].colliderect(scorpion_rect):
                scorpion_lives = max(0, scorpion_lives - 1)
                knives.remove(k)
                if scorpion_lives <= 0:
                    scorpion_active = False
                continue

    # spike mechanics
        for s in spikes[:]:
            s['rect'].x += s['vx']
            if s['rect'].right < 0 or s['rect'].left > width:
                spikes.remove(s)
                continue
            if scorpion_active and s['rect'].colliderect(scorpion_rect):
                scorpion_lives = max(0, scorpion_lives - 1)
                spikes.remove(s)
                if scorpion_lives <= 0:
                    scorpion_active = False
                    continue

    # lala attack
        if lala_alive:
            lala_slime_timer -= 1
            if lala_slime_timer <= 0:
                if scorpion_active:
                    tx, ty = scorpion_rect.center
                    target_flag = 'scorpion'
                else:
                    tx, ty = player_rect.center
                    target_flag = 'player'
                lx, ly = lala_rect.center
                dx = tx - lx
                dy = ty - ly
                dist = (dx*dx + dy*dy) ** 0.5
                if dist == 0:
                    dist = 1
                vx = (dx / dist) * lala_slime_speed
                vy = (dy / dist) * lala_slime_speed
                s = {
                    'x': lx - lala_slime_img.get_width() / 2,
                    'y': ly - lala_slime_img.get_height() / 2,
                    'vx': vx,
                    'vy': vy,
                    'rect': lala_slime_img.get_rect(center=(int(lx), int(ly))),
                    'target': target_flag,
                    'age': 0 
                }
                lala_slimes.append(s)
                lala_slime_timer = random.randint(
                    lala_slime_min_cd, lala_slime_max_cd)

    # lala attack, colliding
        for l in lala_slimes[:]:
            l['x'] += l['vx']
            l['y'] += l['vy']
            l['age'] += 1  
            l['rect'].topleft = (int(l['x']), int(l['y']))
            if l['rect'].right < 0 or l['rect'].left > width or l['rect'].bottom < 0 or l['rect'].top > height:
                try:
                    lala_slimes.remove(l)
                except ValueError:
                    pass
                continue
            if l.get('target') == 'scorpion' and scorpion_active and l['rect'].colliderect(scorpion_rect):
                scorpion_lives = max(0, scorpion_lives - 1)
                try:
                    lala_slimes.remove(l)
                except ValueError:
                    pass
                if scorpion_lives <= 0:
                    scorpion_active = False
                continue
            if l.get('target') == 'player' and l['rect'].colliderect(player_rect):
                if not player_invulnerable:
                    damage = 1 + (l.get('age', 0) // 120)
                    damage = min(damage, 5)
                    player_lives = max(0, player_lives - damage)
                    player_invulnerable = True
                    invulnerable_timer = invulnerable_frames
                try:
                    lala_slimes.remove(l)
                except ValueError:
                    pass
                continue

    # scorpion attack, colliding
        for p in poison_spews[:]:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['rect'].topleft = (int(p['x']), int(p['y']))
            if p['rect'].right < 0 or p['rect'].left > width or p['rect'].bottom < 0 or p['rect'].top > height:
                poison_spews.remove(p)
                continue
            if p['rect'].colliderect(player_rect):
                if not player_invulnerable:
                    player_lives = max(0, player_lives - poison_damage)
                    player_invulnerable = True
                    invulnerable_timer = invulnerable_frames
                try:
                    poison_spews.remove(p)
                except ValueError:
                    pass
                continue

    # fight mechanics
        if lala_alive and lala_rect.colliderect(player_rect):
            if not player_invulnerable:
                player_lives -= 1
                player_lives = max(0, player_lives)
                player_invulnerable = True
                invulnerable_timer = invulnerable_frames

        if player_invulnerable:
            invulnerable_timer -= 1
            if invulnerable_timer <= 0:
                player_invulnerable = False

        if axe_timer > 0:
            axe_timer -= 1

        # handle axe enchant timer
        if axe_enchanted and axe_enchant_timer > 0:
            axe_enchant_timer -= 1
            if axe_enchant_timer <= 0:
                axe_enchanted = False

        if scorpion_ever_active and (not scorpion_active) and (not first_fight_done):
            first_fight_done = True
            if tree_img is not None:
                trees = create_trees_for_room(current_room)

        if player_lives <= 0:
            reset_game_state()
            continue

        in_water = any(player_rect.colliderect(w) for w in water_rects)
        if prev_in_water and (not in_water):
            #if rooms[current_room].get("has_lala", False) and lala_alive:
            # enchanting
            def display_enchanting_panel(surface):
                paneltwo_w, paneltwo_h = 700, 400
                paneltwo_x, paneltwo_y = 100, height - panel_h - 100
                paneltwo_rect = pygame.Rect(paneltwo_x, paneltwo_y, paneltwo_w, paneltwo_h)
                pygame.draw.rect(surface, (300, 300, 300), paneltwo_rect)
                pygame.draw.rect(surface, (500, 500, 500), paneltwo_rect, 3)

                title = instr_font.render("Enchanting (O to toggle)", True, (250, 250, 250))
                surface.blit(title, (paneltwo_x + 20, paneltwo_y + 16))

                enchant_text = font.render("Enchant Axe: Axe + LaLa's poison", True, (230, 230, 230))
                surface.blit(enchant_text, (paneltwo_x + 20, paneltwo_y + 60))
 
                axe_count = count_item_in_inventory(ITEM_AXE)
                poison_count = count_item_in_inventory(ITEM_POISON)
                ac = font.render(f"Axe: {axe_count}", True, (230, 230, 230))
                pc = font.render(f"Poison: {poison_count}", True, (230, 230, 230))
                surface.blit(ac, (paneltwo_x + 20, paneltwo_y + 140))
                surface.blit(pc, (paneltwo_x + 20, paneltwo_y + 180))

                able_to_enchant = axe_count >= 1 and poison_count >= 1
                btntwo_w, btntwo_h = 120, 36
                btntwo_x, btntwo_y = paneltwo_x + paneltwo_w - btntwo_w - 12, paneltwo_y + panel_h - btntwo_h - 12
                btn_rect = pygame.Rect(btntwo_x, btntwo_y, btntwo_w, btntwo_h)
                pygame.draw.rect(surface, (100, 180, 100) if able_to_enchant else (90, 90, 90), btn_rect)
                btn_text = font.render("Enchant Axe", True, (10, 10, 10))
                surface.blit(btn_text, (btntwo_x + (btntwo_w - btn_text.get_width()) // 2,
                btntwo_y + (btntwo_h - btn_text.get_height()) // 2))


        if dialogue_done and lala_alive:
            for i in range(lala_lives):
                x = width - 10 - heart_img.get_width() - i * (heart_img.get_width() + 5)
                y = 10
                screen.blit(heart_img, (x, y))
            if lala_lives <= 0:
                lala_alive = False

        for k in knives:
            screen.blit(knife_img, k['rect'])

        for s in spikes:
            screen.blit(spike_img, s['rect'])

        for l in lala_slimes:
            screen.blit(lala_slime_img, l['rect'])

        for g in lulu_slimes:
            screen.blit(lulu_slime_img, g['rect'])

        for p in poison_spews:
            screen.blit(poison_img, p['rect'])

        if scorpion_active:
            screen.blit(scorpion_img, scorpion_rect)
            bar_w = scorpion_img.get_width()
            bar_h = 6
            bar_x = scorpion_rect.left
            bar_y = scorpion_rect.top - bar_h - 4
            if bar_w > 0:
                health_ratio = scorpion_lives / \
                    float(rooms[current_room].get(
                        "scorpion_lives", max(1, scorpion_lives)))
                pygame.draw.rect(screen, (120, 120, 120),
                                 (bar_x, bar_y, bar_w, bar_h))
                pygame.draw.rect(screen, (200, 50, 50), (bar_x,
                                 bar_y, int(bar_w * health_ratio), bar_h))

        # raft movement
        player_on_raft = False
        for r in raft_objects:
            if player_rect.colliderect(r['rect']):
                player_on_raft = True
                if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    r['rect'].x += speed
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    r['rect'].x -= speed
                # limit raft to screen
                r['rect'].x = max(0, min(width - r['rect'].width, r['rect'].x))

        # water detection (drowning)
        if in_water and not player_on_raft:
            player_breath -= 1
            if player_breath <= 0:
                player_lives = 0
            # breath bar
            bar_w = 160
            bar_h = 10
            bx = (width - bar_w) // 2
            by = 50
            pygame.draw.rect(screen, (40, 40, 40), (bx, by, bar_w, bar_h))
            breath_ratio = max(0, player_breath) / float(breath_max)
            pygame.draw.rect(screen, (50, 150, 230),
                             (bx, by, int(bar_w * breath_ratio), bar_h))
        else:
            # restore breath
            player_breath = min(player_breath + 2, breath_max)

        if player_invulnerable and (invulnerable_timer // 6) % 2 == 0:
            pass
        else:
            screen.blit(player, player_rect)

        # show enchant/poison HUD
        if axe_enchanted:
            ench_time_s = max(0, axe_enchant_timer // 60)
            ench_surf = instr_font.render(f"Axe enchanted (+{AXE_ENCHANT_BONUS} dmg) {ench_time_s}s", True, (200, 180, 40))
            screen.blit(ench_surf, (10, height - 100))
        if poisoned_from_lala:
            p_time_s = max(0, lala_poison_timer // 60)
            poison_surf = font.render(f"Poisoned by LaLa: {p_time_s}s", True, (180, 40, 40))
            screen.blit(poison_surf, (10, height - 130))

        #life bar
        heart_w = heart_img.get_width()
        spacing = 5
        for i in range(player_lives):
            x = 10 + i * (heart_w + spacing)
            y = 10
            screen.blit(heart_img, (x, y))

        pygame.mouse.set_visible(True)
        render_inventory(screen, mouse_pos, equipped_index)

        for item in dropped_items:
            screen.blit(item['img'], item['rect'])

        # crafting UI
        craft_button_rect = None
        raft_button_rect = None
        if is_crafting_open:
            craft_button_rect, raft_button_rect = display_crafting_panel(
                screen)

    # movement
    if game_state == "main":
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_rect.x += speed
            facing = "right"
            move_direction = MoveDirection.MOVE_RIGHT
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_rect.x -= speed
            facing = "left"
            move_direction = MoveDirection.MOVE_LEFT
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and player_rect.y > 220:
            player_rect.y -= speed
            move_direction = MoveDirection.MOVE_UP
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player_rect.y += speed
            move_direction = MoveDirection.MOVE_DOWN

        if player_rect.left >= width:
            if current_room < len(rooms) - 1:
                enter_room(current_room + 1, from_right=False)
            else:
                player_rect.right = width - 1

        if player_rect.right <= 0:
            if current_room > 0:
                enter_room(current_room - 1, from_right=True)
            else:
                player_rect.left = 0

        if player_rect.top < 0:
            player_rect.top = 0
        if player_rect.bottom > height:
            player_rect.bottom = height

    elif game_state == "forest":
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_rect.x += speed
            facing = "right"
            move_direction = MoveDirection.MOVE_RIGHT
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_rect.x -= speed
            facing = "left"
            move_direction = MoveDirection.MOVE_LEFT
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and player_rect.y > 0:
            player_rect.y -= speed
            move_direction = MoveDirection.MOVE_UP
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player_rect.y += speed
            move_direction = MoveDirection.MOVE_DOWN
        
        # Grenzen
        player_rect.left = max(0, player_rect.left)
        player_rect.right = min(width, player_rect.right)
        player_rect.top = max(0, player_rect.top)
        player_rect.bottom = min(height, player_rect.bottom)
        
        # Zum Ufer gehen (rechts rausgehen)
        if player_rect.right >= width:
            game_state = "raft_building"
            player_rect.bottomleft = (100, 750)

    elif game_state == "raft_building":
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_rect.x += speed
            facing = "right"
            move_direction = MoveDirection.MOVE_RIGHT
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_rect.x -= speed
            facing = "left"
            move_direction = MoveDirection.MOVE_LEFT
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and player_rect.y > 0:
            player_rect.y -= speed
            move_direction = MoveDirection.MOVE_UP
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player_rect.y += speed
            move_direction = MoveDirection.MOVE_DOWN
        
        # Grenzen
        player_rect.left = max(0, player_rect.left)
        player_rect.right = min(width, player_rect.right)
        player_rect.top = max(0, player_rect.top)
        player_rect.bottom = min(height, player_rect.bottom)

    elif game_state == "boss_fight":
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_rect.x += speed
            facing = "right"
            move_direction = MoveDirection.MOVE_RIGHT
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_rect.x -= speed
            facing = "left"
            move_direction = MoveDirection.MOVE_LEFT
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and player_rect.y > 0:
            player_rect.y -= speed
            move_direction = MoveDirection.MOVE_UP
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player_rect.y += speed
            move_direction = MoveDirection.MOVE_DOWN
        
        # Boss Attacken (Skorpion schießt Gift auf Spieler)
        if boss_active and random.random() < 0.01:
            bx, by = boss_rect.center
            px, py = player_rect.center
            dx = px - bx
            dy = py - by
            dist = (dx*dx + dy*dy) ** 0.5
            if dist == 0:
                dist = 1
            vx = (dx / dist) * poison_speed
            vy = (dy / dist) * poison_speed
            p = {
                'x': bx - poison_img.get_width() / 2,
                'y': by - poison_img.get_height() / 2,
                'vx': vx,
                'vy': vy,
                'rect': poison_img.get_rect(center=(int(bx), int(by)))
            }
            poison_spews.append(p)
        
        # Boss Attacken bewegen und prüfen
        for p in poison_spews[:]:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['rect'].topleft = (int(p['x']), int(p['y']))
            if p['rect'].right < 0 or p['rect'].left > width or p['rect'].bottom < 0 or p['rect'].top > height:
                poison_spews.remove(p)
                continue
            if p['rect'].colliderect(player_rect):
                if not player_invulnerable:
                    player_lives = max(0, player_lives - poison_damage)
                    player_invulnerable = True
                    invulnerable_timer = invulnerable_frames
                try:
                    poison_spews.remove(p)
                except ValueError:
                    pass
                continue
        
        # Messer Attacken prüfen
        for k in knives[:]:
            k['rect'].x += k['vx']
            if k['rect'].right < 0 or k['rect'].left > width:
                knives.remove(k)
                continue
            if boss_active and k['rect'].colliderect(boss_rect):
                boss_lives = max(0, boss_lives - 1)
                knives.remove(k)
                continue
        
        # Grenzen
        player_rect.left = max(0, player_rect.left)
        player_rect.right = min(width, player_rect.right)
        player_rect.top = max(0, player_rect.top)
        player_rect.bottom = min(height, player_rect.bottom)

    elif game_state == "scorpion_fight":
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_rect.x += speed
            facing = "right"
            move_direction = MoveDirection.MOVE_RIGHT
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_rect.x -= speed
            facing = "left"
            move_direction = MoveDirection.MOVE_LEFT
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and player_rect.y > 0:
            player_rect.y -= speed
            move_direction = MoveDirection.MOVE_UP
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player_rect.y += speed
            move_direction = MoveDirection.MOVE_DOWN
        
        # Skorpion Attacken
        if scorpion_active and random.random() < 0.01:
            sx, sy = scorpion_rect.center
            px, py = player_rect.center
            dx = px - sx
            dy = py - sy
            dist = (dx*dx + dy*dy) ** 0.5
            if dist == 0:
                dist = 1
            vx = (dx / dist) * poison_speed
            vy = (dy / dist) * poison_speed
            p = {
                'x': sx - poison_img.get_width() / 2,
                'y': sy - poison_img.get_height() / 2,
                'vx': vx,
                'vy': vy,
                'rect': poison_img.get_rect(center=(int(sx), int(sy)))
            }
            poison_spews.append(p)
        
        # Skorpion Attacken bewegen
        for p in poison_spews[:]:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['rect'].topleft = (int(p['x']), int(p['y']))
            if p['rect'].right < 0 or p['rect'].left > width or p['rect'].bottom < 0 or p['rect'].top > height:
                poison_spews.remove(p)
                continue
            if p['rect'].colliderect(player_rect):
                if not player_invulnerable:
                    player_lives = max(0, player_lives - poison_damage)
                    player_invulnerable = True
                    invulnerable_timer = invulnerable_frames
                try:
                    poison_spews.remove(p)
                except ValueError:
                    pass
                continue
        
        # Messer prüfen
        for k in knives[:]:
            k['rect'].x += k['vx']
            if k['rect'].right < 0 or k['rect'].left > width:
                knives.remove(k)
                continue
            if scorpion_active and k['rect'].colliderect(scorpion_rect):
                scorpion_lives = max(0, scorpion_lives - 1)
                knives.remove(k)
                if scorpion_lives <= 0:
                    scorpion_active = False
                continue
        
        # Grenzen
        player_rect.left = max(0, player_rect.left)
        player_rect.right = min(width, player_rect.right)
        player_rect.top = max(0, player_rect.top)
        player_rect.bottom = min(height, player_rect.bottom)

    if is_quest_box_shown:
        display_quest_box(screen)
        pygame.display.update()
        clock.tick(60)

    # raft crafting rendering (if active, draw overlay and palette)
    if raft_crafting:
        # dim background
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))
        # drawing area
        area = get_raft_area_rect()
        area_w, area_h = area.width, area.height
        area_x, area_y = area.x, area.y
        pygame.draw.rect(screen, (200, 200, 180),
                         (area_x, area_y, area_w, area_h))
        pygame.draw.rect(screen, (100, 100, 100),
                         (area_x, area_y, area_w, area_h), 3)
        # title and instructions
        title = title_font.render("Raft Assembly", True, (10, 10, 10))
        screen.blit(title, (area_x + 12, area_y + 8))
        instr = font.render(
            "Drag planks from the palette and arrange them into a connected raft. Q/E rotate. Press T to tie (needs 3 resin). Esc to cancel.", True, (10, 10, 10))
        screen.blit(instr, (area_x + 12, area_y + 70))
        # draw placed planks (rotated)
        for pl in placed_planks:
            img = pygame.transform.rotate(plank_img, pl.get('angle', 0))
            img_rect = img.get_rect(center=pl['rect'].center)
            # if it's currently selected, draw highlight
            if pl is selected_plank:
                # semi-opaque preview when moving
                temp = img.copy()
                temp.set_alpha(220)
                screen.blit(temp, img_rect)
                pygame.draw.rect(screen, (30, 160, 30), img_rect, 2)
            else:
                screen.blit(img, img_rect)
                pygame.draw.rect(screen, (80, 50, 20), img_rect, 2)
        # draw palette
        pal_text = font.render("Palette:", True, (10, 10, 10))
        screen.blit(pal_text, (40, height - 230))
        for p in raft_palette:
            # show plank image clipped to palette rect
            img_rect = plank_img.get_rect(center=p['rect'].center)
            screen.blit(plank_img, img_rect)
            if p['used']:
                pygame.draw.rect(screen, (120, 120, 120), p['rect'], 3)
            else:
                pygame.draw.rect(screen, (30, 160, 30), p['rect'], 3)
        # draw snap grid
        for cx, cy in get_snap_cells():
            pygame.draw.circle(screen, (150, 150, 150),
                               (int(cx), int(cy)), 6, 1)
        # draw tie button
        tie_rect = pygame.Rect(area_x + area_w - 140,
                               area_y + area_h - 60, 120, 40)
        pygame.draw.rect(screen, (100, 180, 100), tie_rect)
        tie_text = font.render("Tie (T)", True, (10, 10, 10))
        screen.blit(tie_text, (tie_rect.x + 20, tie_rect.y + 10))
        # cancel button
        cancel_rect = pygame.Rect(
            area_x + area_w - 300, area_y + area_h - 60, 120, 40)
        pygame.draw.rect(screen, (180, 100, 100), cancel_rect)
        cancel_text = font.render("Cancel (Esc)", True, (10, 10, 10))
        screen.blit(cancel_text, (cancel_rect.x + 6, cancel_rect.y + 10))
        pygame.display.update()
        clock.tick(60)
        continue

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
