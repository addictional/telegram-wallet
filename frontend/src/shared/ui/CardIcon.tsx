import MasterCardIcon from '@/assets/mastercard.svg?react';
import  VisaIcon from '@/assets/visa.svg?react'
import  MirIcon from '@/assets/mir.svg?react'
import {Card} from '@/shared/const'
import type {CardType} from '@/shared/types'

type CardIconProps = React.SVGProps<SVGSVGElement> & {
  cardType: CardType
}

export const CardIcon = ({cardType,...props}: CardIconProps) =>  {
  switch(cardType) {
    case Card.MasterCard: 
      return <MasterCardIcon {...props}/>
    case Card.Visa:
      return <VisaIcon {...props}/>
    default:
      return <MirIcon {...props}/>    
  }
}