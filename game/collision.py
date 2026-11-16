
def check_bullet_meteor_collisions(bullets, meteors):
    destroyed_meteors = 0

    for bullet in bullets[:]:
        for meteor in meteors[:]:

            if bullet.rect.colliderect(meteor.rect):

                bullets.remove(bullet)
                meteor.health -= 1

                if meteor.health <= 0:
                    meteors.remove(meteor)
                    destroyed_meteors += 1

                break

    return destroyed_meteors
