import AngleHelper from "@/utils/AngleHelper";
import clsx from "clsx";
import { useEffect, useRef, useState } from "react";

export type AngleSliderProps = {
    scrollStep?: number;
    onChange?: (angle: number) => void;
    angle: number;
    isDegrees?: boolean;
    fineAdjustment?: number;
}

export default function AngleSlider({ scrollStep = 0.1, onChange, angle, isDegrees, fineAdjustment = 1 }: AngleSliderProps) {
    const lineLength = 72;
    const containerRef = useRef<HTMLDivElement>(null);
    const [isDragging, setIsDragging] = useState(false);
    const [dragInitialAngle, setDragInitialAngle] = useState(0);

    useEffect(() => {
        if (containerRef.current) {
            containerRef.current.onwheel = (e) => {
                e.preventDefault();
                if (e.deltaY > 0) {
                    onChange?.(angle - scrollStep * fineAdjustment);
                } else {
                    onChange?.(angle + scrollStep * fineAdjustment);
                }
            };


            containerRef.current.onmousedown = (e) => {
                e.preventDefault();
                setIsDragging(true);
                if (!containerRef.current) return;
                const middleX = containerRef.current?.getBoundingClientRect().x + containerRef.current?.getBoundingClientRect().width / 2;
                const middleY = containerRef.current?.getBoundingClientRect().y + containerRef.current?.getBoundingClientRect().height / 2;
                setDragInitialAngle(AngleHelper.angleBetweenPointsInRadians(middleX, middleY, e.x, e.y,));
            };

            document.onmouseup = (e) => {
                setIsDragging(false);
            };

            document.onmousemove = (e) => {
                if (!containerRef.current) return;
                if (isDragging) {
                    const middleX = containerRef.current?.getBoundingClientRect().x + containerRef.current?.getBoundingClientRect().width / 2;
                    const middleY = containerRef.current?.getBoundingClientRect().y + containerRef.current?.getBoundingClientRect().height / 2;

                    let difference = AngleHelper.angleBetweenPointsInRadians(middleX, middleY, e.x, e.y) - dragInitialAngle;
                    if (Math.abs(difference) > Math.PI) {
                        difference = difference > 0 ? difference - 2 * Math.PI : difference + 2 * Math.PI;
                    }
                    onChange?.(angle + ((isDegrees ? AngleHelper.radianToDegree(difference) : difference) * Math.max(0.125, Math.min(1, fineAdjustment))));
                    setDragInitialAngle(AngleHelper.angleBetweenPointsInRadians(middleX, middleY, e.x, e.y));
                }

            };
        }
    }, [containerRef, angle, isDragging, fineAdjustment]);

    return (
        <div ref={containerRef} className={clsx("max-w-2xs w-fit mx-auto m-4 bg-blue-100 rounded-full shadow-md")}>
            <svg width="144px" height="144px" viewBox="0 0 144 144">
                <g>
                    <line x1="50%" y1="90%" x2="50%" y2="100%" stroke="#bababa" strokeWidth="2" />
                    <line x1="50%" y1="10%" x2="50%" y2="0%" stroke="#bababa" strokeWidth="2" />
                    <line x1="90%" y1="50%" x2="100%" y2="50%" stroke="#bababa" strokeWidth="2" />
                    <line x1="10%" y1="50%" x2="0%" y2="50%" stroke="#bababa" strokeWidth="2" />
                </g>
                <g style={{ transformOrigin: 'center', transform: 'rotate(45deg)' }} >
                    <line x1="50%" y1="90%" x2="50%" y2="100%" stroke="#bababa" strokeWidth="2" />
                    <line x1="50%" y1="10%" x2="50%" y2="0%" stroke="#bababa" strokeWidth="2" />
                    <line x1="90%" y1="50%" x2="100%" y2="50%" stroke="#bababa" strokeWidth="2" />
                    <line x1="10%" y1="50%" x2="0%" y2="50%" stroke="#bababa" strokeWidth="2" />
                </g>
                <g style={{ transformOrigin: 'center', transform: 'rotate(22.5deg)' }}>
                    <line x1="50%" y1="93%" x2="50%" y2="100%" stroke="#cbcbcb" strokeWidth="1" />
                    <line x1="50%" y1="7%" x2="50%" y2="0%" stroke="#cbcbcb" strokeWidth="1" />
                    <line x1="93%" y1="50%" x2="100%" y2="50%" stroke="#cbcbcb" strokeWidth="1" />
                    <line x1="7%" y1="50%" x2="0%" y2="50%" stroke="#cbcbcb" strokeWidth="1" />
                </g>
                <g style={{ transformOrigin: 'center', transform: 'rotate(-22.5deg)' }}>
                    <line x1="50%" y1="93%" x2="50%" y2="100%" stroke="#cbcbcb" strokeWidth="1" />
                    <line x1="50%" y1="7%" x2="50%" y2="0%" stroke="#cbcbcb" strokeWidth="1" />
                    <line x1="93%" y1="50%" x2="100%" y2="50%" stroke="#cbcbcb" strokeWidth="1" />
                    <line x1="7%" y1="50%" x2="0%" y2="50%" stroke="#cbcbcb" strokeWidth="1" />
                </g>
                <line x1="50%" y1="50%" x2={72 + lineLength * Math.cos((isDegrees ? AngleHelper.degreeToRadian(angle) : angle) - Math.PI / 2)} y2={72 + lineLength * Math.sin((isDegrees ? AngleHelper.degreeToRadian(angle) : angle) - Math.PI / 2)} stroke="#969696" strokeWidth="2" />

            </svg>
        </div>
    )
}