
def check_bullet_meteor_collisions(bullets, meteors):

    destroyed_positions = []

    for bullet in bullets[:]:

        for meteor in meteors[:]:

            if bullet.rect.colliderect(meteor.rect):

                bullets.remove(bullet)

                meteor.health -= 1

                if meteor.health <= 0:

                    destroyed_positions.append(
                        meteor.rect.center
                    )

                    meteors.remove(meteor)

                break

    return destroyed_positions


def check_bullet_boss_collisions(bullets, boss):

    for bullet in bullets[:]:

        if bullet.rect.colliderect(boss.rect):

            bullets.remove(bullet)
            boss.take_damage(1)

    return boss.health <= 0


def check_boss_hazard_collisions(player, hazards):

    damage = 0

    for hazard in hazards[:]:

        if hazard.collides_with(player):

            damage += hazard.damage

            if hazard.kind in ("projectile", "homing"):
                hazards.remove(hazard)

    return damage
