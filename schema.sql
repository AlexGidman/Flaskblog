drop table if exists user;
CREATE TABLE "user" ( "id" INTEGER NOT NULL, "username" TEXT NOT NULL, "password" TEXT NOT NULL, PRIMARY KEY("id" AUTOINCREMENT) )
drop table if exists posts;
CREATE TABLE "posts" ( "id" INTEGER NOT NULL, "user_id" INTEGER NOT NULL, "title" TEXT NOT NULL, "content" TEXT NOT NULL, "date_posted" TEXT NOT NULL, PRIMARY KEY("id"), FOREIGN KEY("user_id") REFERENCES "user"("id") )
drop table if exists profile;
CREATE TABLE "profile" ( "id" INTEGER NOT NULL, "user_id" INTEGER NOT NULL, "first" TEXT NOT NULL, "last" TEXT NOT NULL, "profession" TEXT NOT NULL, "interests" TEXT NOT NULL, PRIMARY KEY("id" AUTOINCREMENT), FOREIGN KEY("user_id") REFERENCES "user"("id") )