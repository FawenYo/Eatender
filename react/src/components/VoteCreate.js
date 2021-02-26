import React from 'react'
import styled from "styled-components";
import { motion } from "framer-motion";
import { Paper, makeStyles } from "@material-ui/core"

import VoteCreateForm from "./VoteCreateForm";

const AppContainer = styled.div`
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
`;

const BoxContainer = styled.div`
  width: 330px;
  min-height: 550px;
  display: flex;
  flex-direction: column;
  border-radius: 19px;
  background-color: #fff;
  box-shadow: 0 0 2px rgba(15, 15, 15, 0.28);
  position: relative;
  overflow: hidden;
`;

const TopContainer = styled.div`
  width: 100%;
  height: 185px;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding: 0 1.8em;
  padding-bottom: 5em;
`;

const HeaderContainer = styled.div`
  width: 100%;
  display: flex;
  flex-direction: column;
`;

const BannerText = styled.h2`
  font-size: 40px;
  font-weight: 600;
  line-height: 1.25;
  color: #fff;
  z-index: 10;
  margin: 0;
`;

const HeaderText = styled.h2`
  font-size: 30px;
  font-weight: 600;
  line-height: 1.25;
  color: #fff;
  z-index: 10;
  margin: 0;
`;

const SmallText = styled.h5`
  color: #c24510;
  font-weight: 1000 !important;
  font-size: 13px;
  z-index: 10;
  margin: 0;
  margin-top: 7px;
`;

const BackDrop = styled(motion.div)`
  width: 140%;
  height: 550px;
  position: absolute;
  display: flex;
  flex-direction: column;
  border-radius: 50%;
  transform: rotate(60deg);
  top: -290px;
  left: -70px;
  background: rgb(241, 196, 15);
  background: linear-gradient(
    58deg,
    rgba(250, 215, 87, 1) 20%,
    rgba(243, 172, 18, 1) 100%
  );
`;

const useStyles = makeStyles(theme => ({
    pageContent: {
        margin: theme.spacing(5),
        padding: theme.spacing(3),
    }
}))


function VoteCreate() {

    const classes = useStyles();

    return (
        <AppContainer>
            <BoxContainer>
                <TopContainer>
                    <BackDrop
                        initial={false}
                    />
                    <HeaderContainer>
                        <BannerText>EATender</BannerText>
                        <HeaderText>聚餐創立</HeaderText>
                        <SmallText>加LINE約吃飯，感情不會散！</SmallText>
                    </HeaderContainer>
                </TopContainer>
                    <VoteCreateForm />
            </BoxContainer>
        </AppContainer>
    )
}

export default VoteCreate
