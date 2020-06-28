# data_gestion_genders.py
# OM 2020.04.09 Permet de gérer (CRUD) les données de la table t_genders

from flask import flash
from APP_PIECES_D_OCCASIONS.DATABASE.connect_db_context_manager import MaBaseDeDonnee
from APP_PIECES_D_OCCASIONS.DATABASE.erreurs import *


class GestionStateStuff:
    def __init__(self):
        try:
            # DEBUG bon marché : Pour afficher un message dans la console.
            print("dans le try de gestions genders")
            # OM 2020.04.11 La connexion à la base de données est-elle active ?
            # Renvoie une erreur si la connexion est perdue.
            MaBaseDeDonnee().connexion_bd.ping(False)
        except Exception as erreur:
            flash("Dans Gestion genders ...terrible erreur, il faut connecter une base de donnée", "Danger")
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(f"Exception grave Classe constructeur GestionGenders {erreur.args[0]}")
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurConnexion(f"{msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[0]}")
        print("Classe constructeur GestionGenders ")

    def state_stuff_afficher_data(self, valeur_order_by, id_state_stuff_sel):
        try:
            with MaBaseDeDonnee().connexion_bd.cursor() as mc_afficher:
                if valeur_order_by == "ASC" and id_state_stuff_sel == 0:
                    strsql_state_stuff_afficher = """SELECT id_state_stuff, state_stuff FROM t_state_stuff ORDER BY id_state_stuff ASC"""
                    mc_afficher.execute(strsql_state_stuff_afficher)
                elif valeur_order_by == "ASC":
                    # OM 2020.04.07 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_genders"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du gender sélectionné avec un nom de variable
                    valeur_id_genders_selected_dictionnaire = {"value_id_state_stuff_selected": id_state_stuff_sel}
                    strsql_state_stuff_afficher = """SELECT id_state_stuff, state_stuff FROM t_state_stuff  WHERE id_state_stuff = %(value_id_state_stuff_selected)s"""
                    # Envoi de la commande MySql
                    mc_afficher.execute(strsql_state_stuff_afficher, valeur_id_state_stuff_selected_dictionnaire)
                else:
                    strsql_state_stuff_afficher = """SELECT id_state_stuff, state_stuff FROM t_state_stuff ORDER BY id_state_stuff DESC"""
                    # Envoi de la commande MySql
                    mc_afficher.execute(strsql_state_stuff_afficher)
                    # Récupère les données de la requête.
                data_state_stuff = mc_afficher.fetchall()
                # Affichage dans la console
                print("data_state_stuff ", data_state_stuff, " Type : ", type(data_state_stuff))
                # Retourne les données du "SELECT"
                return data_state_stuff
        except pymysql.Error as erreur:
            print(f"DGG gad pymysql errror {erreur.args[0]} {erreur.args[1]}")
            raise MaBdErreurPyMySl(
                    f"DGG gad pymysql errror {msg_erreurs['ErreurPyMySql']['message']} {erreur.args[0]} {erreur.args[1]}")
        except Exception as erreur:
            print(f"DGG gad Exception {erreur.args}")
            raise MaBdErreurConnexion(f"DGG gad Exception {msg_erreurs['ErreurConnexionBD']['message']} {erreur.args}")
        except pymysql.err.IntegrityError as erreur:
            # OM 2020.04.09 On dérive "pymysql.err.IntegrityError" dans le fichier "erreurs.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurConnexion(f"DGG gad pei {msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[1]}")

    def add_state_stuff_data(self, valeurs_insertion_dictionnaire):
        try:
            print(valeurs_insertion_dictionnaire)
            # OM 2020.04.07 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            strsql_insert_state_stuff = """INSERT INTO t_state_stuff (id_state_stuff,state_stuff) VALUES (NULL,%(value_state_stuff)s)"""
            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee() as mconn_bd:
                mconn_bd.mabd_execute(strsql_insert_state_stuff, valeurs_insertion_dictionnaire)

        except pymysql.err.IntegrityError as erreur:
            # OM 2020.04.09 On dérive "pymysql.err.IntegrityError" dans "MaBdErreurDoublon" fichier "erreurs.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurDoublon(
                f"DGG pei erreur doublon {msg_erreurs['ErreurDoublonValue']['message']} et son status {msg_erreurs['ErreurDoublonValue']['status']}")

    def edit_state_stuff_data(self, valeur_id_dictionnaire):
        try:
            print(valeur_id_dictionnaire)
            # OM 2020.04.07 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # Commande MySql pour afficher le gender sélectionné dans le tableau dans le formulaire HTML
            str_sql_id_state_stuff = """SELECT id_state_stuff, state_stuff FROM t_state_stuff WHERE id_state_stuff = %(value_id_state_stuff)s"""

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_id_state_stuff, valeur_id_dictionnaire)
                    data_id_state_stuff = mc_cur.fetchall()
                    print("valeur_id_dictionnaire...", data_id_state_stuff)
                    return data_id_state_stuff

        except Exception as erreur:
            # OM 2020.03.01 Message en cas d'échec du bon déroulement des commandes ci-dessus.
            print(f"Problème edit_gender_data Data Gestions Genders numéro de l'erreur : {erreur}")
            # flash(f"Flash. Problèmes Data Gestions Genders numéro de l'erreur : {erreur}", "danger")
            # OM 2020.04.09 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise Exception(
                "Raise exception... Problème edit_gender_data d'un gender Data Gestions Genders {erreur}")

    def update_state_stuff_data(self, valeur_update_dictionnaire):
        try:
            print(valeur_update_dictionnaire)
            # OM 2019.04.02 Commande MySql pour la MODIFICATION de la valeur "CLAVIOTTEE" dans le champ "nameEditIntituleGenderHTML" du form HTML "GendersEdit.html"
            # le "%s" permet d'éviter des injections SQL "simples"
            # <td><input type = "text" name = "nameEditIntituleGenderHTML" value="{{ row.intitule_gender }}"/></td>
            str_sql_update_gender = "UPDATE t_state_stuff SET state_stuff = %(value_state_stuff)s WHERE id_state_stuff = %(value_id_state_stuff)s"

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_update_state_stuff, valeur_update_dictionnaire)

        except (Exception,
                pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                pymysql.IntegrityError,
                TypeError) as erreur:
            # OM 2020.03.01 Message en cas d'échec du bon déroulement des commandes ci-dessus.
            print(f"Problème update_gender_data Data Gestions Genders numéro de l'erreur : {erreur}")
            # flash(f"Flash. Problèmes Data Gestions Genders numéro de l'erreur : {erreur}", "danger")
            # raise Exception('Raise exception... Problème update_gender_data d\'un gender Data Gestions Genders {}'.format(str(erreur)))
            if erreur.args[0] == 1062:
                flash(f"Flash. Cette valeur existe déjà : {erreur}", "danger")
                # Deux façons de communiquer une erreur causée par l'insertion d'une valeur à double.
                flash('Doublon !!! Introduire une valeur différente')
                # Message en cas d'échec du bon déroulement des commandes ci-dessus.
                print(f"Problème update_gender_data Data Gestions Genders numéro de l'erreur : {erreur}")

                raise Exception("Raise exception... Problème update_gender_data d'un gender DataGestionsGenders {erreur}")

    def delete_select_state_stuff_data(self, valeur_delete_dictionnaire):
        try:
            print(valeur_delete_dictionnaire)
            # OM 2019.04.02 Commande MySql pour la MODIFICATION de la valeur "CLAVIOTTEE" dans le champ "nameEditIntituleGenderHTML" du form HTML "GendersEdit.html"
            # le "%s" permet d'éviter des injections SQL "simples"
            # <td><input type = "text" name = "nameEditIntituleGenderHTML" value="{{ row.intitule_gender }}"/></td>

            # OM 2020.04.07 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # Commande MySql pour afficher le gender sélectionné dans le tableau dans le formulaire HTML
            str_sql_select_id_state_stuff = "SELECT id_state_stuff, state_stuff FROM t_state_stuff WHERE id_state_stuff = %(value_id_state_stuff)s"

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une gméthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_select_id_state_stuff, valeur_delete_dictionnaire)
                    data_one = mc_cur.fetchall()
                    print("valeur_id_dictionnaire...", data_one)
                    return data_one

        except (Exception,
                pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                pymysql.IntegrityError,
                TypeError) as erreur:
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(f"Problème delete_select_state_stuff_data Gestions state_stuff numéro de l'erreur : {erreur}")
            # C'est une erreur à signaler à l'utilisateur de cette application WEB.
            flash(f"Flash. Problème delete_select_state_stuff_data numéro de l'erreur : {erreur}", "danger")
            raise Exception(
                "Raise exception... Problème delete_select_state_stuff_data d\'un state_stuff Data Gestions state_stuff {erreur}")

    def delete_state_stuff_data(self, valeur_delete_dictionnaire):
        try:
            print(valeur_delete_dictionnaire)
            # OM 2019.04.02 Commande MySql pour EFFACER la valeur sélectionnée par le "bouton" du form HTML "GendersEdit.html"
            # le "%s" permet d'éviter des injections SQL "simples"
            # <td><input type = "text" name = "nameEditIntituleGenderHTML" value="{{ row.intitule_gender }}"/></td>
            str_sql_delete_state_stuff = "DELETE FROM t_state_stuff WHERE id_state_stuff = %(value_id_state_stuff)s"

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_delete_state_stuff, valeur_delete_dictionnaire)
                    data_one = mc_cur.fetchall()
                    print("valeur_id_dictionnaire...", data_one)
                    return data_one
        except (Exception,
                pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                pymysql.IntegrityError,
                TypeError) as erreur:
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(f"Problème delete_gender_data Data Gestions Genders numéro de l'erreur : {erreur}")
            # flash(f"Flash. Problèmes Data Gestions Genders numéro de l'erreur : {erreur}", "danger")
            if erreur.args[0] == 1451:
                # OM 2020.04.09 Traitement spécifique de l'erreur 1451 Cannot delete or update a parent row: a foreign key constraint fails
                # en MySql le moteur INNODB empêche d'effacer un gender qui est associé à un film dans la table intermédiaire "t_genders_films"
                # il y a une contrainte sur les FK de la table intermédiaire "t_genders_films"
                # C'est une erreur à signaler à l'utilisateur de cette application WEB.
                # flash(f"Flash. IMPOSSIBLE d'effacer !!! Ce gender est associé à des user dans la t_genders_films !!! : {erreur}", "danger")
                # DEBUG bon marché : Pour afficher un message dans la console.
                print(
                    f"IMPOSSIBLE d'effacer !!! Ce gender est associé à des films dans la t_state_stuff !!! : {erreur}")
            raise MaBdErreurDelete(f"DGG Exception {msg_erreurs['ErreurDeleteContrainte']['message']} {erreur}")
