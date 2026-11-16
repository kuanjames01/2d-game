
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
