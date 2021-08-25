const bcrypt = require("bcrypt");
const passport = require("passport");
// const mongoose = require("mongoose");

const localStrategy = require("passport-local").Strategy;
const JWTstrategy = require("passport-jwt").Strategy;
const ExtractJWT = require("passport-jwt").ExtractJwt;

const db = require("../controllers/databaseController.js");

const UserModel = require("../models/userModel.js");

const User = db.collection("user");

passport.use(
    "signup",
    new localStrategy(
        {
            usernameField: "username",
            passwordField: "password",
            passReqToCallback: true,
        },
        async (req, username, password, done) => {
            try {
                const exist = await User.findOne({ username: username });
                if (exist == null) {
                    const hash = await bcrypt.hash(
                        password,
                        parseInt(process.env.SALT)
                    );
                    const newUser = new UserModel({
                        username: username,
                        password: hash,
                        isAdmin: req.body.isAdmin,
                        firstName: req.body.firstName,
                        lastName: req.body.lastName,
                    });
                    await User.insertOne(newUser);
                    return done(null, newUser);
                } else {
                    return done("Error: User already exists!");
                }
            } catch (error) {
                done(error);
            }
        }
    )
);

passport.use(
    "login",
    new localStrategy(
        {
            usernameField: "username",
            passwordField: "password",
        },
        async (username, password, done) => {
            try {
                console.log(username, password);
                const user = await User.findOne({
                    username: username,
                });

                if (user == null) {
                    return done(null, false, { message: "User not found" });
                }

                const validate = await bcrypt.compare(password, user.password);

                if (!validate) {
                    return done(null, false, { message: "Wrong Password" });
                }

                return done(null, user, { message: "Logged in Successfully" });
            } catch (error) {
                return done(error);
            }
        }
    )
);

passport.use(
    new JWTstrategy(
        {
            secretOrKey: process.env.SECRET_KEY,
            jwtFromRequest: ExtractJWT.fromAuthHeaderWithScheme("JWT"),
        },
        async (token, done) => {
            try {
                return done(null, token.user);
            } catch (error) {
                done(error);
            }
        }
    )
);
